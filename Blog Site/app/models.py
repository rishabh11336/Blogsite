"""Database models."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model with improved security and relationships."""
    
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    contact_no = db.Column(db.String(15), unique=True, nullable=False)
    sex = db.Column(db.String(6), nullable=False)
    profile_pic = db.Column(db.String(255), nullable=False, default='default.jpg')
    bio = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic',
                          cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='user', lazy='dynamic',
                          cascade='all, delete-orphan')
    following = db.relationship('Following',
                              foreign_keys='Following.follower_id',
                              backref=db.backref('follower', lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')
    followers = db.relationship('Following',
                              foreign_keys='Following.followed_id',
                              backref=db.backref('followed', lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')

    @property
    def password(self):
        """Prevent password from being accessed."""
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """Set password to a hashed password."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Check if hashed password matches actual password."""
        return check_password_hash(self.password_hash, password)

    def follow(self, user):
        """Follow a user."""
        if not self.is_following(user):
            f = Following(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        """Unfollow a user."""
        f = self.following.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        """Check if following a user."""
        return self.following.filter_by(
            followed_id=user.id).first() is not None

    def followed_posts(self):
        """Get posts from followed users."""
        followed = Post.query.join(
            Following, (Following.followed_id == Post.user_id)
        ).filter(Following.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.created_at.desc())

class Post(db.Model):
    """Post model with improved structure."""
    
    __tablename__ = 'post'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    likes = db.relationship('Like', backref='post', lazy='dynamic',
                          cascade='all, delete-orphan')

    def to_dict(self):
        """Convert post to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author.name,
            'image': self.image,
            'created_at': self.created_at.isoformat(),
            'likes_count': self.likes.count()
        }

class Like(db.Model):
    """Like model with improved structure."""
    
    __tablename__ = 'like'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='_post_user_uc'),)

class Following(db.Model):
    """Following model with improved structure."""
    
    __tablename__ = 'following'
    
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('follower_id', 'followed_id', name='_follower_followed_uc'),
    )