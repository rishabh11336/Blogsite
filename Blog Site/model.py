from main import db
from sqlalchemy.sql import func

#Model

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key = True)
    email = db.Column(db.String(100))
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))  
    contact_no = db.Column(db.Integer)
    sex = db.Column(db.String(6))
    profile_pic = db.Column(db.String)  #to save url for pics
    bio = db.Column(db.String(250))

class Like(db.Model):
    __tablename__ = 'like'
    like_id = db.Column(db.Integer, primary_key = True,  nullable=False)
    post_id = db.Column(db.Integer,   db.ForeignKey("post.post_id"), nullable=False)
    name = db.Column(db.String,   db.ForeignKey("user.name"), nullable=False)

class Following(db.Model):
    __tablename__ = 'following'
    follow_id = db.Column(db.Integer, primary_key=True, nullable=False)
    id = db.Column(db.Integer,   db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String,   db.ForeignKey("user.name"), nullable=False)
    following = db.Column(db.String,   db.ForeignKey("user.name"), nullable=False)
    following_id = db.Column(db.Integer,   db.ForeignKey("user.id"), nullable=False)
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
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,   db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, primary_key = True,  nullable=False)
    post = db.Column(db.String(250))
    name = db.Column(db.String,   db.ForeignKey("user.name"), nullable=False)
    image = db.Column(db.String)
    time = db.Column(db.DateTime(timezone=True), server_default=func.now())