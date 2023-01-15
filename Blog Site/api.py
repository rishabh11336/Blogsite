from flask_restful import Resource
from flask import request
from main import db
from model import *

#UserAPI for CRUD
class UserAPI(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if user:
                return {'email': user.email,
                'name': user.name,
                'sex': user.sex,
                'conatct': user.contact_no,
                'Bio': user.bio,
                'Image': "127.0.0.1:8080/static/"+user.profile_pic}, 200
            else:
                return {'message': 'User not found'}, 404

    def post(self):
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        password = data.get('password')
        profile_pic = 'temp.jpg'
        sex = 'Other'
        bio = 'write about yourself'
        contact_no = 1111111111

        # check if user with email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {'message': 'User with email already exists'}, 409

        # create new user
        password = password
        user = User(email=email, name=name, password=password, profile_pic=profile_pic, sex=sex, bio=bio, contact_no=contact_no)
        db.session.add(user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201

    def put(self, user_id):
        data = request.get_json()
        name = data.get('name')
        password = data.get('password')
        email = data.get('email')
        contact_no = data.get('contact_no')
        bio = data.get('bio')
        sex = data.get('sex')

        # check if user exists
        user = User.query.filter_by(id=user_id).first()
        if user:
            user.name = name
            user.password = password
            user.email = email
            user.contact_no = contact_no
            user.bio = bio
            user.sex =sex
            db.session.commit()
            return {'message': 'User updated successfully'}, 201
        else:
            return {'message': 'User not found'}, 404

    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        follows = Following.query.filter_by(id=user_id)
        posts = Post.query.filter_by(id=user_id)
        likes = Like.query.filter_by(user_id=user_id)
        for like in likes:
            if like:
                db.session.delete(like)
                #db.session.commit()
        for post in posts:
            if post:
                db.session.delete(post)
                #db.session.commit()
        for follow in follows:
            if follow:
                db.session.delete(follow)
                #db.session.commit()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}, 200
        else:
            return {'message': 'User not found'}, 404

#Post/Blog API for CRUD
class PostAPI(Resource):
    def get(self, post_id=None):
        if post_id:
            post = Post.query.filter_by(post_id=post_id).first()
            if post:
                if post.image:
                    return {"post_id":post.post_id,
                    "user_id": post.id,
                    "username": post.name,
                    "title": post.title,
                    "blog": post.post,
                    "image": "127.0.0.1:8080/static/"+post.image,
                    "time": str(post.time)}, 200
                else:
                    return {"post_id":post.post_id,
                "user_id": post.id,
                "username": post.name,
                "title": post.title,
                "blog": post.post,
                "time": str(post.time)}, 200
            else:
                return {'message': 'Post not found'}, 404

    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        post_text = data.get('post')
        post_image = "temp.jpg"
        post_title = data.get('title')
        user_name = data.get('name')
        time = datetime.utcnow()

        post = Post(id=user_id, post=post_text, image=post_image, title=post_title, name=user_name, time=time)
        db.session.add(post)
        db.session.commit()

        return {'message': 'Post created successfully'}, 201

    def put(self, post_id):
        data = request.get_json()
        post_text = data.get('post')
        post_title = data.get('title')

        post = Post.query.filter_by(post_id=post_id).first()
        if post:
            post.post = post_text
            post.title = post_title
            db.session.commit()
            return {'message': 'Post updated successfully'}
        else:
            return {'message': 'Post not found'}, 404

    def delete(self, post_id):
        post = Post.query.filter_by(post_id=post_id).first()
        likes = Like.query.filter_by(post_id=post_id)
        for like in likes:
            if like:
                db.session.delete(like)
        if post:
            db.session.delete(post)
            db.session.commit()
            return {'message': 'Post deleted successfully'}
        else:
            return {'message': 'Post not found'}, 404