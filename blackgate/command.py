# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .connection_pool import ConnectionPool

# FIXME: declare pools
from .core import pools

class Command(object):

    # FIXME: find a better way to declare group_key
    group_key = None

    # FIXME: find a better place to create connection pool
    connection_pool = ConnectionPool()

    def run(self):
        raise NotImplementedError

    def fallback(self):
        return

    def submit(self):
        # FIXME: define get_executor_pool for pools
        executor = pools.get_executor(self.group_key)
        # FIXME: limit executor queue length
        try:
            future = executor.submit(self.run)
        except pools.CircuitBeakerRejectError:
            future = self.fallback()
        return future
