# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .connection_pool import ConnectionPool

from .core import component

class Command(object):

    # FIXME: find a better way to declare group_key
    group_key = 'default'

    command_key = None

    # FIXME: find a better place to create connection pool
    connection_pool = ConnectionPool()

    def run(self):
        raise NotImplementedError

    def fallback(self):
        raise NotImplementedError

    def execute(self):
        # TODO: implement cache machenism.

        if not component.circuit_beaker.is_allow_request(self.group_key, self.command_key):
            return self.fallback()

        executor = component.pools.get_executor(self.group_key)

        try:
            future = executor.submit(self.run)
            component.circuit_beaker.report_success(self.group_key, self.command_key)

        except component.pools.PoolFull:
            future = self.fallback()
            component.circuit_beaker.report_reject(self.group_key, self.command_key)

        except component.pools.ExecutionTimeout:
            future = self.fallback()
            component.circuit_beaker.report_timeout(self.group_key, self.command_key)

        except component.pools.ExecutionFailure:
            future = self.fallback()
            component.circuit_beaker.report_failure(self.group_key, self.command_key)

        return future
