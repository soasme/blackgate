# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json
import logging
import socket
from urllib import urlencode

from tornado import gen, queues
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError

from blackgate.core import component

logger = logging.getLogger(__name__)

class Command(object):

    def __init__(self, request, proxy):
        self.proxy = proxy
        self.request = request
        self.response = {}

    @gen.coroutine
    def async(self):
        client = AsyncHTTPClient()
        self.before_request()
        request = HTTPRequest(
            url='%s?%s' % (self.request['url'], urlencode(self.request['params'])),
            method=self.request['method'].upper(),
            headers=self.request['headers'],
            body=self.request['data'] if self.request['method'].upper() != 'GET' else None,
            connect_timeout=self.options.get('connect_timeout_seconds'),
            request_timeout=self.options.get('timeout_seconds'),
        )
        try:
            resp = yield client.fetch(request)
            self.response = dict(
                status_code=resp.code,
                reason=resp.reason,
                headers=dict(resp.headers),
                content=resp.body,
            )
        except HTTPError as error:
            self.response = dict(
                status_code=error.code,
                reason=error.response.reason,
                headers=dict(error.response.headers),
                content=resp.response.body,
            )
        self.after_response()
        raise gen.Return(self.response)

    def fallback(self, reason=''):
        return dict(
            status_code=502,
            reason='Bad Gateway',
            headers={
                'Content-Type': 'application/json',
            },
            content=json.dumps({
                'code': 502,
                'message': str(reason) or 'gateway is using fallback mechanism',
                'errors': []
            })
        )

    @property
    def options(self):
        return dict(
            group_key=self.proxy['name'],
            command_key='proxy',
            timeout_seconds=self.proxy.get('timeout_seconds') or 30,
            connect_timeout_seconds=self.proxy.get('connect_timeout_seconds') or 3,
            timeout_enabled=bool(self.proxy.get('timeout_enabled')),
       )

    @property
    def circuit_beaker(self):
        return component.get_circuit_beaker(
            self.options.get('command_key'),
            self.options.get('group_key'),
            component.circuit_beaker_impl,
            **component.circuit_beaker_options
        )

    @gen.coroutine
    def queue(self):
        # TODO: implement cache machenism.
        circuit_beaker = self.circuit_beaker
        group_key = self.options.get('group_key')
        executor = component.pools.get_executor(group_key)

        if not circuit_beaker.allow_request():
            result = self.fallback('gateway reject due to circuit beaker open.')
            logger.error('type: circuit_beaker_reject')
            raise gen.Return(result)

        try:
            result = yield executor.submit(self.async)
            circuit_beaker.mark_success() # FIXME: this should be async, possibly network error

        except socket.error:
            result = self.fallback('gateway failed to connect upstream.')
            circuit_beaker.mark_timeout()
            logger.error('type: socket_error')

        except queues.QueueFull:
            result = self.fallback('gateway reject due to too many connections.')
            circuit_beaker.mark_reject()
            logger.error('type: pool_full')

        except gen.TimeoutError:
            result = self.fallback('gateway timeout on fetching upstream.')
            circuit_beaker.mark_timeout()
            logger.error('type: execution_timeout')

        # FIXME: catch more exceptions: submit failure, wrong timeout type, mark_success run failed.

        except Exception as exception: # FIXME: only network error should fallback, others crash it??
            # XXX: use some error aggreation system like sentry to report errors???
            result = self.fallback()
            circuit_beaker.mark_failure()
            import traceback
            traceback.print_exc()

        raise gen.Return(result)


    def before_request(self):
        return

    def after_response(self):
        return
