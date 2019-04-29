#!/usr/bin/env python
# coding: utf-8
# author: wyi

ENV = 'dev'


class Config(object):
    SECRET_KEY = '9et^n)e^!yggrah0900i05ygcb22fu-q%2ci967a52z@(3jn86'


class DevConfig(Config):
    # DB
    DB_HOST = '192.168.217.128'
    DB_PORT = 3306
    DB_NAME = 'uPool'
    DB_USER = 'admin'
    DB_PASS = '123456'
    # DB Pool
    DB_POOL_MAX_CONN = 5
    # others


class PrdConfig(Config):
    # DB
    DB_HOST = '172.16.2.161'
    DB_PORT = 3306
    DB_NAME = 'uPool'
    DB_USER = 'admin'
    DB_PASS = '123@456'
    # DB Pool
    DB_POOL_MAX_CONN = 5
    # others


config = {
    'dev': DevConfig,
    'prd': PrdConfig
}
