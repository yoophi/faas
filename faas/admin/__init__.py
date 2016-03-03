#!/usr/bin/env python
# coding: utf-8

import os
import os.path as op

from flask import Flask
from flask.ext.config_helper import Config
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask_admin import Admin
from flask_admin.contrib import sqla

from faas.models import db, Client

CURRENT_DIR = op.abspath(op.dirname(__file__))
TEMPLATE_DIR = op.join(CURRENT_DIR, 'templates')
STATIC_DIR = op.join(CURRENT_DIR, 'static')

debug_toolbar = DebugToolbarExtension()

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

config = Config()
config.init_app(app)
debug_toolbar.init_app(app)

app.config.from_yaml(config_name=(os.getenv('FLASK_CONFIG') or 'default'),
                     file_name='app.yml',
                     search_paths=[op.dirname(op.dirname(app.root_path))])

db.init_app(app)

admin = Admin(app, name='Admin', template_mode='bootstrap3')

admin.add_view(sqla.ModelView(Client, name='Client', session=db.session))


if __name__ == '__main__':
    app.run(debug=True)