# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging

import requests
from tornado import gen
from tornado.ioloop import IOLoop
from concurrent.futures import TimeoutError

from blackgate.core import component

logger = logging.getLogger(__name__)

class Command(object):

    # FIXME: find a better way to declare group_key
    group_key = 'default'

    command_key = None

    def run(self):
        raise NotImplementedError

    def fallback(self):
        raise NotImplementedError

    @gen.coroutine
    def queue(self):
        # TODO: implement cache machenism.
        circuit_beaker = component.get_circuit_beaker(
            self.command_key,
            self.group_key,
            component.circuit_beaker_impl,
            **component.circuit_beaker_options
        )

        if not circuit_beaker.allow_request():
            future = self.fallback()
            raise gen.Return(future)

        executor = component.pools.get_executor(self.group_key)

        try:
            future = yield executor.submit(self.run)
            circuit_beaker.mark_success()

        except component.pools.PoolFull:
            future = self.fallback()
            circuit_beaker.mark_reject()
            logger.error('type: pool_full')

        except TimeoutError:
            future = self.fallback()
            circuit_beaker.mark_timeout()
            logger.error('type: execution_timeout')

        except Exception as exception:
            future = self.fallback()
            circuit_beaker.mark_failure()
            logger.error('type: execution_fail, reason: %s', exception.message)

        raise gen.Return(future)

    def execute(self):
        try:
            return self.run()
        except Exception as exception:
            logger.error('type: execution_fail, reason: %s', exception.message)
            return self.fallback()


class HTTPProxyCommand(Command):

    def __init__(self, request):
        self.request = request
        self.response = {}

    def before_request(self):
        return

    def after_response(self):
        return

    def run(self):
        session = requests.Session()
        self.before_request()
        resp = session.request(
            method=self.request['method'].upper(),
            url=self.request['url'],
            params=self.request['params'],
            data=self.request['data'],
            headers=self.request['headers'],
        )
        self.response = dict(
            status_code=resp.status_code,
            reason=resp.reason,
            headers=dict(resp.headers),
            content=resp.content
        )
        self.after_response()
        return self.response
