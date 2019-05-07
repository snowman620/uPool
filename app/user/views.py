#!/usr/bin/env python
# coding: utf-8
# author: wyi

from . import user
from flask import jsonify
from app.utils import db_pool
from gevent import queue


@user.route('/list', methods=['GET'])
def user_list():
    """demo"""
    try:
        conn = db_pool.get_conn()
        results = conn.query_all('SELECT `id`,`name` FROM `tb1`')
        return jsonify({'code': 1, 'msg': 'ok', 'data': [{'id': n[0], 'name': n[1]} for n in results]})
    except queue.Empty:
        # do something
        return jsonify({'code': 0, 'msg': 'queue empty'})
    except Exception as e:
        # do something
        return jsonify({'code': 0, 'msg': 'error'})
