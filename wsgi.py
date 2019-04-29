#!/usr/bin/env python
# coding: utf-8
# author: wyi

from gevent import monkey
monkey.patch_socket()

from flask_script import Manager
from cmd import Test
from app import create_app
import json

app = create_app()

manager = Manager(app)
manager.add_command('test', Test())


@app.route('/')
def status():
    return json.dumps({'code': 1, 'msg': 'API is running'})


if __name__ == '__main__':
    manager.run()
