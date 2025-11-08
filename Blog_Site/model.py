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
    contact_no = db.Column(db.Integer)
    sex = db.Column(db.String(6))
    profile_pic = db.Column(db.Text)  # store data URI or filename for pics
    bio = db.Column(db.String(250))

#Model for like/unlike table
class Like(db.Model):
    __tablename__ = 'like'
    like_id = db.Column(db.Integer, primary_key = True,  nullable=False)
    post_id = db.Column(db.Integer,   db.ForeignKey("post.post_id"), nullable=False)
    user_id = db.Column(db.Integer,   db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String,   db.ForeignKey("user.name"), nullable=False)

#Model for follow/unfollow table
class Following(db.Model):
    __tablename__ = 'following'
    follow_id = db.Column(db.Integer, primary_key=True, nullable=False)
    id = db.Column(db.Integer,   db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String,   db.ForeignKey("user.name"), nullable=False)
    following = db.Column(db.String,   db.ForeignKey("user.name"), nullable=False)
    following_id = db.Column(db.Integer,   db.ForeignKey("user.id"), nullable=False)


# Model for comments
class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String, db.ForeignKey('user.name'), nullable=False)
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
    name = db.Column(db.String,   db.ForeignKey("user.name"), nullable=False)
    image = db.Column(db.Text)  # store data URI or filename for post image
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationship: comments for this post
    comments = db.relationship('Comment', backref='post_parent', lazy='dynamic', cascade='all, delete-orphan')
