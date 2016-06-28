# -*- coding: utf-8 -*-

import re
import logging

from tornado import gen, web
from blackgate.command import Command

logger = logging.getLogger(__name__)

class HTTPProxy(web.RequestHandler):

    def initialize(self, proxy):
        self.proxy = proxy

    @gen.coroutine
    def get(self, *args, **kwargs):
        yield self._fetch(*args, **kwargs)

    @gen.coroutine
    def post(self, *args, **kwargs):
        yield self._fetch(*args, **kwargs)

    @gen.coroutine
    def put(self, *args, **kwargs):
        yield self._fetch(*args, **kwargs)

    @gen.coroutine
    def delete(self, *args, **kwargs):
        yield self._fetch(*args, **kwargs)

    @gen.coroutine
    def patch(self, *args, **kwargs):
        yield self._fetch(*args, **kwargs)

    @gen.coroutine
    def head(self, *args, **kwargs):
        yield self._fetch(*args, **kwargs)

    @gen.coroutine
    def options(self, *args, **kwargs):
        yield self._fetch(*args, **kwargs)

    @gen.coroutine
    def _fetch(self, *args, **kwargs):
        headers = dict(self.request.headers.get_all())
        headers.pop('Host', None)
        headers['User-Agent'] = 'Blackgate/0.1.0'
        path = re.sub(
            self.proxy['request_path_regex'],
            self.proxy['request_path_sub'],
            self.request.path
        )
        upstream_url = self.proxy['upstream_url']
        url = upstream_url + path
        request_data = dict(
            method=self.request.method,
            url=url,
            params=self.request.query_arguments,
            data=self.request.body,
            headers=headers,
        )
        logger.debug('request: %s' % request_data)

        command = Command(request_data, self.proxy)
        resp = yield command.queue()

        logger.debug('response: %s' % resp)
        self.write_resp(resp)

    def write_resp(self, resp):
        self.set_status(resp['status_code'], resp['reason'])

        for k, v in resp['headers'].items():
            if k in {
                    'Server',
                    'Content-Encoding',
                    'Content-Length',
                    'Transfer-Encoding',
            }:
                continue

            if k == 'Set-Cookie': # FIXME: support multiple set-cookie in headers.
                self.add_header(k, v)
                continue

            self.set_header(k, v)

        if resp['content']:
            self.write(resp['content'])
