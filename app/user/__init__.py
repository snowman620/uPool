#!/usr/bin/env python
# coding: utf-8
# author: wyi

from flask import Blueprint

user = Blueprint('user', __name__)

from . import views
