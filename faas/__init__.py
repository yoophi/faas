#!/usr/bin/env python
# coding: utf-8
import os

from flask import Flask

from flask.ext.config_helper import Config
from flask.ext.cors import CORS
from flask.ext.login import LoginManager
from flask.ext.oauthlib.provider import OAuth2Provider

from .models import db, User

__version__ = '0.1'

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

config= Config()
oauth = OAuth2Provider()
cors = CORS()

def create_app(config_name):
    """
    :param config_name: developtment, production or testing
    :return: flask application

    flask application generator
    """
    template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app = Flask(__name__, template_folder=template_folder)
    config.init_app(app)
    app.config.from_yaml(config_name=config_name,
                         file_name='app.yml',
                         search_paths=[os.path.dirname(app.root_path)])
    app.config.from_heroku(keys=['SQLALCHEMY_DATABASE_URI', ])

    cors.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    oauth.init_app(app)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api as api_1_0_blueprint

    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app


@login_manager.user_loader
def load_user(user_id):
    """Hook for Flask-Login to load a User instance from a user ID."""
    return User.query.get(user_id)
