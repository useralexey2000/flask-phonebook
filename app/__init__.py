import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import config
import click
from flask.cli import AppGroup


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view= 'auth.login'
from app.models import AnonymousUser
login_manager.anonymous_user = AnonymousUser

db_cli = AppGroup('db')

def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=True)

    if config_name is None:
        app.config.from_object(config['default'])
    else:
        app.config.from_object(config[config_name])
        config[config_name].init_app(app)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    """Init extentions and register blueprints"""
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    app.cli.add_command(db_cli)

    from app import errors
    app.register_blueprint(errors.bp)

    from app import pbook
    app.register_blueprint(pbook.bp)

    from app import auth
    app.register_blueprint(auth.bp)

    from app import admin
    app.register_blueprint(admin.bp)

    app.add_url_rule('/', endpoint='index')

    return app

@db_cli.command('init')
def init_db():
    """Command to recreate db"""
    db.drop_all()
    db.create_all()
