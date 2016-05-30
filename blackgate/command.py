# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
from copy import deepcopy
from datetime import timedelta

import requests
from tornado import gen, queues
from tornado.ioloop import IOLoop
from concurrent.futures import TimeoutError

from blackgate.core import component

logger = logging.getLogger(__name__)

class Command(object):

    __command_args__ = {
        'group_key': 'default',
        'command_key': None,
        'timeout_seconds': 1,
        'timeout_enabled': True,
    }

    def run(self):
        raise NotImplementedError

    def fallback(self):
        raise NotImplementedError

    @property
    def circuit_beaker(self):
        return component.get_circuit_beaker(
            self.options.get('command_key'),
            self.options.get('group_key'),
            component.circuit_beaker_impl,
            **component.circuit_beaker_options
        )

    @property
    def options(self):
        if hasattr(self, '_options'):
            return self._options

        args = deepcopy(Command.__command_args__)
        args.update(self.__command_args__)
        setattr(self, '_options', args)

        return args

    @gen.coroutine
    def queue(self):
        # TODO: implement cache machenism.
        circuit_beaker = self.circuit_beaker
        timeout_enabled = self.options.get('timeout_enabled')
        timeout_seconds = self.options.get('timeout_seconds')
        group_key = self.options.get('group_key')

        if not circuit_beaker.allow_request():
            result = self.fallback()
            logger.error('type: circuit_beaker_reject')
            raise gen.Return(result)

        executor = component.pools.get_executor(group_key)

        try:
            timeout_seconds = timeout_seconds if timeout_enabled else 30 # FIXME
            timeout = timedelta(seconds=timeout_seconds)
            result = yield gen.with_timeout(timeout, executor.submit(self.run))
            circuit_beaker.mark_success()

        except queues.QueueFull:
            result = self.fallback()
            circuit_beaker.mark_reject()
            logger.error('type: pool_full')

        except gen.TimeoutError:
            result = self.fallback()
            circuit_beaker.mark_timeout()
            logger.error('type: execution_timeout')

        except Exception as exception:
            result = self.fallback()
            circuit_beaker.mark_failure()
            logger.error('type: execution_fail, reason: %s', exception.message)

        raise gen.Return(result)

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
