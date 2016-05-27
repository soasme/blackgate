# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor

class ExecutorPools(object):

    class PoolFull(Exception):
        pass

    class ExecutionTimeout(Exception):
        pass

    class ExecutionFailure(Exception):
        pass

    def __init__(self):
        self.pools = {}

    def register_pool(self, group_key, max_workers=1):
        self.pools[group_key] = ThreadPoolExecutor(max_workers=max_workers)

    def get_executor(self, group_key):
        if group_key not in self.pools:
            raise Exception("Pool not registerd")
        return self.pools[group_key]
