from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

current_dir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = 'static/'

app = Flask(__name__)

# Database Configuration - PostgreSQL (Supabase) or SQLite fallback
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    "sqlite:///" + os.path.join(current_dir, "database.sqlite3")

# PostgreSQL connection pool settings
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 60,          # Reduced from 300 to 60
    'pool_size': 10,
    'max_overflow': 20,
    'pool_timeout': 30,          # Added explicit timeout
    'connect_args': {
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 16777216))

db = SQLAlchemy()
db.init_app(app)
api = Api(app)
app.app_context().push()

# Session configuration - use environment variable secret key
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24)


#Model
#from model import *
 
#controller
from controller import *

# #All restfulAPI controler
# from api import UserAPI, PostAPI
# api.add_resource(UserAPI, '/users/', '/users/<int:user_id>')
# api.add_resource(PostAPI, '/posts/', '/posts/<int:post_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)