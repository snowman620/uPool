#!/usr/bin/env python
# coding: utf-8
# author: wyi

from flask import Flask
from config import config, ENV


def create_app():
    app = Flask(__name__)
    app.config.from_object(config[ENV])
    app.app_context().push()

    from .user import user as user__blueprint
    app.register_blueprint(user__blueprint, url_prefix='/user')

    return app
