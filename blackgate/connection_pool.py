# -*- coding: utf-8 -*-

import time

import requests


class ConnectionPool(object):

    def __init__(self, conn_reuse_count=100, conn_reuse_duration=60):
        self._pool = {}
        self.conn_reuse_count = conn_reuse_count
        self.conn_reuse_duration = conn_reuse_duration

    def get_connection(self, host):
        if host in self._pool:
            conn_info = self._pool[host]
            if (conn_info['count'] < self.conn_reuse_count and
                time.time() - conn_info['time'] < self.conn_reuse_duration):
                conn_info['count'] += 1
                conn = conn_info['conn']
                conn.cookies.clear()
                return conn

        conn = requests.session()

        conn_info = {
            'conn': conn,
            'count': 0,
            'time': time.time()
        }
        self._pool[host] = conn_info

        return conn
