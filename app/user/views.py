#!/usr/bin/env python
# coding: utf-8
# author: wyi

from . import user
from app.utils import db_pool
from gevent import queue
import json


@user.route('/list', methods=['GET'])
def user_list():
    """demo"""
    try:
        conn = db_pool.get_conn()
        results = conn.query_all('SELECT `id`,`name` FROM `tb1`')
        return json.dumps({'code': 1, 'msg': 'ok', 'data': [{'id': n[0], 'name': n[1]} for n in results]})
    except queue.Empty:
        # do something
        return json.dumps({'code': 0, 'msg': 'queue empty'})
    except Exception as e:
        # do something
        return json.dumps({'code': 0, 'msg': 'error'})
