from main import db
from datetime import date, datetime, timedelta
from sqlalchemy import func

#Model
#Model for User table
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key = True)
    email = db.Column(db.String(100))
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))  
    contact_no = db.Column(db.BigInteger)  # Changed to BigInteger for large phone numbers
    sex = db.Column(db.String(6))
    profile_pic = db.Column(db.Text)  # store data URI or filename for pics
    bio = db.Column(db.String(250))
    
    # Indexes for query performance
    __table_args__ = (
        db.Index('idx_user_email', 'email'),
        db.Index('idx_user_name', 'name'),
    )

#Model for like/unlike table
class Like(db.Model):
    __tablename__ = 'like'
    like_id = db.Column(db.Integer, primary_key = True,  nullable=False)
    post_id = db.Column(db.Integer,   db.ForeignKey("post.post_id"), nullable=False)
    user_id = db.Column(db.Integer,   db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String)  # Stores username for display - no FK to avoid constraint issues
    
    # Prevent duplicate likes
    __table_args__ = (
        db.UniqueConstraint('post_id', 'user_id', name='unique_post_user_like'),
    )

#Model for follow/unfollow table
class Following(db.Model):
    __tablename__ = 'following'
    follow_id = db.Column(db.Integer, primary_key=True, nullable=False)
    id = db.Column(db.Integer,   db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String)  # Follower name - no FK to avoid constraint issues
    following = db.Column(db.String)  # Followed user name - no FK to avoid constraint issues
    following_id = db.Column(db.Integer,   db.ForeignKey("user.id"), nullable=False)
    
    # Prevent duplicate follows
    __table_args__ = (
        db.UniqueConstraint('id', 'following_id', name='unique_follower_followed'),
    )


# Model for comments
class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String)  # Stores commenter name for display - no FK to avoid constraint issues
    comment = db.Column(db.String(500))
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # optional: repr
    def __repr__(self):
        return f"<Comment {self.comment_id} by {self.name}>"

#for Mad-2 project not implemented yet 
'''
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer,   db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.Integer,   db.ForeignKey("user.name"), nullable=False)
    comment_id = db.Column(db.Integer, primary_key = True, nullable=False)
    post_id = db.Column(db.Integer,   db.ForeignKey("user.id"), nullable=False)
    comment = db.Column(db.String(250))
    time = db.Column(db.DateTime(timezone=True), server_default=func.now())
'''

#Model for blog/post table
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,   db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, primary_key = True,  nullable=False)
    title = db.Column(db.String)
    post = db.Column(db.String)
    name = db.Column(db.String)  # Stores author name for display - no FK to avoid constraint issues
    image = db.Column(db.Text)  # store data URI or filename for post image
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationship: comments for this post
    comments = db.relationship('Comment', backref='post_parent', lazy='dynamic', cascade='all, delete-orphan')
    
    # Indexes for query performance
    __table_args__ = (
        db.Index('idx_post_user_id', 'id'),
        db.Index('idx_post_time', 'time'),
    )
