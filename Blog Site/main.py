from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import os

current_dir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = 'static/'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "database.sqlite3")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
db = SQLAlchemy()
db.init_app(app)
api = Api(app)
app.app_context().push()
#session
app.secret_key=os.urandom(24)


#Model
#from model import *
db.init_app(app)
app.app_context().push()
 
#controller
from controller import *

#All restful controler
from api import UserAPI
api.add_resource(UserAPI, '/users/', '/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)