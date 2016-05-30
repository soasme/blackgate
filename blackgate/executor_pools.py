# -*- coding: utf-8 -*-

from blackgate.executor import QueueExecutor
from tornado.ioloop import IOLoop


class ExecutorPools(object):

    def __init__(self):
        self.pools = {}

    def register_pool(self, group_key, max_size=10, max_workers=10, ioloop=None):
        executor = QueueExecutor(pool_key=group_key, max_size=max_size, max_workers=max_workers)
        ioloop = ioloop or IOLoop.current()
        ioloop.spawn_callback(executor.consume)
        self.pools[group_key] = executor

    def get_executor(self, group_key):
        if group_key not in self.pools:
            raise Exception("Pool not registerd")
        return self.pools[group_key]
