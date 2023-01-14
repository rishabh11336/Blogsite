from flask_restful import Resource
from flask import request
from main import db
from model import *

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
                'Image': "127.0.0.1:5000"+user.profile_pic}, 200
            else:
                return {'message': 'User not found'}, 404
        else:
            users = User.query.all()
            return [user.to_dict() for user in users]

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