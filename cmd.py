#!/usr/bin/env python
# coding: utf-8
# author: wyi

from flask_script import Command


class Test(Command):
    def run(self):
        print('cmd is ok')
