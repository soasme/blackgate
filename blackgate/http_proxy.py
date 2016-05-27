# -*- coding: utf-8 -*-

from tornado import gen, web

class HTTPProxy(web.RequestHandler):

    def initialize(self, command):
        self.command= command

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
        request_data = dict(
            method=self.request.method,
            path=self.request.path,
            params=self.request.query_arguments,
            data=self.request.body,
            headers=dict(self.request.headers.get_all())
        )
        command = self.command(request_data)
        resp = yield command.execute()
        self.write_resp(resp)

    def write_resp(self, resp):
        self.set_status(resp['status_code'], resp['reason'])

        for k, v in resp['headers'].items():
            if k in {
                    'Server',
                    'Content-Encoding',
                    'Content-Length',
            }:
                continue

            if k == 'Set-Cookie':
                self.add_header(k, v)
                continue

            self.set_header(k, v)

        self.write(resp['content'])
