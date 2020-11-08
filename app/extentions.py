# from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


db = MongoEngine()
login_manager = LoginManager()
bc = Bcrypt()