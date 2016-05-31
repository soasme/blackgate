# -*- coding: utf-8 -*-

import sys
from concurrent.futures import ThreadPoolExecutor
from tornado import gen, queues
from tornado.concurrent import Future, run_on_executor

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

class QueueExecutor(object):

    def __init__(self, pool_key, max_size, max_workers):
        self._pool_key = pool_key
        self._max_size = max_size
        self._max_workers = max_workers
        self._work_queue = queues.Queue(max_size)
        self._work_executor = ThreadPoolExecutor(max_workers)

    def submit(self, fn, *args, **kwargs):
        future = Future()
        item = WorkItem(future, fn, args, kwargs)
        self._work_queue.put_nowait(item)
        return future

    @gen.coroutine
    def consume(self):
        while True:
            try:
                item = yield self._work_queue.get()
                yield self._work_executor.submit(item.run)
            finally:
                self._work_queue.task_done()
