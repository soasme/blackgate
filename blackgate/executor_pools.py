# -*- coding: utf-8 -*-


from tornado.ioloop import IOLoop
from tornado import gen
from blackgate.executor import QueueExecutor
from blackgate.http_client import fetch, handle_client_error

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
            raise Exception("Pool not registerd: %s" % group_key)
        return self.pools[group_key]

    @gen.coroutine
    def execute(self, request, options=None):
        group_key = options.get('name')
        executor = self.get_executor(group_key)
        options = options or {}
        try:
            submit_data = dict(request=request, options=options)
            result = yield executor.submit(fetch, **submit_data)
            raise gen.Return(result)
        except Exception as exc:
            handle_client_error(exc)
