# -*- coding: utf-8 -*-

from tornado.web import Application
from tornado.testing import AsyncHTTPTestCase, gen_test
from blackgate import HTTPProxyCommand, HTTPProxy, component

class TestHTTPProxy(AsyncHTTPTestCase):

    def setUp(self):
        super(TestHTTPProxy, self).setUp()
        component.install()

    def get_app(self):
        class ProxyCommand(HTTPProxyCommand):
            def run(self):
                return dict(
                    status_code=200,
                    reason='OK',
                    headers={
                        'Server': 'SomeServer',
                        'Content-Encoding': 'gzip',
                        'Content-Length': 100,
                        'Set-Cookie': 'a=b',
                    },
                    content='SUCCESS'
                )
        return Application([(r'/', HTTPProxy, dict(command=ProxyCommand))])


    def test_response(self):
        resp = self.fetch('/?a=1')
        assert resp.code == 200
        assert resp.reason == 'OK'
        assert resp.headers.get('Server') != 'SomeServer'
        assert not resp.headers.get('Content-Encoding') # != gzip
        assert resp.headers.get('Content-Length') == str(len('SUCCESS')) # != 100
        assert resp.body == 'SUCCESS'
        assert resp.headers.get('Set-Cookie') == 'a=b'
