#!/usr/python/bin/python3
# -*- coding:utf-8 -*-
############################
#File Name: mysql_threading_pool.py
#Author: ykyk
#Mail: 525178992@qq.com
#Created Time: 2019-01-10 09:17:32
############################

import logging
import Queue
import pymysql
LOG = logging.getLogger(__name__)

class ConnectionPool(object):

    def __init__(self. **kwargs):
        self.size = kwargs.get('size', 10)
        self.kwargs = kwargs
        self.conn_queue = Queue.Queue(maxsize=self.size)

        for i in range(self.size):
            self.conn_queue.put(self._create_new_conn())

    def _create_new_conn(self):
        return pymysql.connect(host=self.kwargs.get('host', '127.0.0.1'),
                               user=self.kwargs.get('user'),
                               passwd=self.kwargs.get('password'),
                               port=self.kwargs.get('port')
                               connect_timeout=5)

    def _put_conn(self, conn):
        self.conn_queue.put(conn)

    def _get_conn(self):
        conn = self.conn_queue.get()
        if conn is None:
            self._create_new_conn()
        return conn

    def exec_sql(self, sql):
        conn = self._get_conn()
        try:
            with conn as cur:
                cur.execute(sql)
                return cur.fetchall()
        except pymysql.ProgrammingError as e:
            LOG.error('execute sql {{0}} error {1}'.format(sql, e))
            raise e
        except pymysql.OperationalError as e:
            conn = self._create_new_conn()
            raise e
        finally:
            self._put_conn(conn)

    def __del__(self):
        try:
            while True:
                conn = self.conn_queue.get_nowait()
                if conn:
                    conn.close()
        except Queue.Empty:
            pass




