# -*- coding: utf-8 -*-

import sys

from concurrent.futures import ThreadPoolExecutor
from tornado import gen, queues
from tornado.concurrent import Future, run_on_executor

from blackgate.http_client import fetch, handle_client_error

class WorkItem(object):

    executor = ThreadPoolExecutor(20)

    def __init__(self, future, fn, args, kwargs):
        self.future = future
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception:
            self.future.set_exc_info(sys.exc_info())
        else:
            self.future.set_result(result)

class AsyncItem(object):

    executor = ThreadPoolExecutor(20)

    def __init__(self, future, fn, args, kwargs):
        self.future = future
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @gen.coroutine
    def run(self):
        try:
            result = yield self.fn(*self.args, **self.kwargs)
        except Exception:
            self.future.set_exc_info(sys.exc_info())
        else:
            self.future.set_result(result)

class QueueExecutor(object):

    def __init__(self, pool_key, max_size):
        self._pool_key = pool_key
        self._max_size = max_size
        self._work_queue = queues.Queue(max_size)

    def submit(self, fn, *args, **kwargs):
        future = Future()
        item = AsyncItem(future, fn, args, kwargs)
        self._work_queue.put_nowait(item)
        return future

    @gen.coroutine
    def consume(self):
        while True:
            try:
                item = yield self._work_queue.get()
                yield item.run()
            finally:
                self._work_queue.task_done()


class ExecutorPools(object):

    def __init__(self):
        self.pools = {}

    def register_pool(self, ioloop, group_key, max_size=10):
        executor = QueueExecutor(pool_key=group_key, max_size=max_size)
        ioloop.spawn_callback(executor.consume)
        self.pools[group_key] = executor
        return executor

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
            result = handle_client_error(exc)
            raise gen.Return(result)
