#!/usr/bin/env python
# coding: utf-8
# author: wyi

from flask import current_app
import gevent
from gevent import queue
import pymysql


class ConnectionPool(object):
    """连接池"""
    def __init__(self):
        self.max_conn = current_app.config['DB_POOL_MAX_CONN']
        self._pool = queue.Queue(maxsize=self.max_conn)
        for _ in range(self.max_conn):
            conn = Connection(
                host=current_app.config['DB_HOST'],
                port=current_app.config['DB_PORT'],
                db=current_app.config['DB_NAME'],
                user=current_app.config['DB_USER'],
                passwd=current_app.config['DB_PASS'],
                charset='utf8'
            )
            conn._pool = self
            self._pool.put_nowait(conn)

    def get_conn(self, retry=3):
        """取出一个连接"""
        try:
            return self._pool.get_nowait()
        except:
            # 重试3次
            gevent.sleep(0.1)
            if retry > 0:
                retry -= 1
                return self.get_conn(retry)
            else:
                raise queue.Empty

    def put_conn(self, conn):
        """存入一个连接"""
        if not conn._pool:
            conn._pool = self
        try:
            self._pool.put_nowait(conn)
        except:
            raise queue.Full

    def size(self):
        """可用连接数"""
        return self._pool.qsize()


class Connection(pymysql.connections.Connection):
    """数据库连接"""
    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)
        self._pool = None

    def _execute(self, query, *args):
        """执行"""
        try:
            cursor = self.cursor()
            cursor.execute(query, *args)
        except pymysql.OperationalError:
            self and self.close()
            self.connect()
            cursor.execute(query, *args)
        return cursor

    def query_all(self, query, *args):
        """查询结果集"""
        cursor = None
        try:
            cursor = self._execute(query, *args)
            return cursor.fetchall()
        finally:
            cursor and cursor.close()
            self._pool.put_conn(self)

    def query_one(self, query, *args):
        """查询单一记录"""
        cursor = None
        try:
            cursor = self._execute(query, *args)
            return cursor.fetchone()
        finally:
            cursor and cursor.close()
            self._pool.put_conn(self)

    def insert(self, query, *args):
        """插入"""
        cursor = None
        try:
            cursor = self._execute(query, *args)
            self.commit()
            row_id = cursor.lastrowid
            return row_id
        except pymysql.IntegrityError:
            self.rollback()
        finally:
            cursor and cursor.close()
            self._pool.put_conn(self)

    def update(self, query, *args):
        """修改"""
        cursor = None
        try:
            cursor = self._execute(query, *args)
            self.commit()
            row_count = cursor.rowcount
            return row_count
        except pymysql.IntegrityError:
            self.rollback()
        finally:
            cursor and cursor.close()
            self._pool.put_conn(self)
