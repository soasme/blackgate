# -*- coding: utf-8 -*-

import json

from mock import patch, MagicMock
from tornado.web import Application
from tornado import gen
from tornado.testing import AsyncHTTPTestCase

from blackgate.component import Component


class TestHTTPProxyFallbackDueToBrokenUpstreamConnection(AsyncHTTPTestCase):

    def get_app(self):
        component = Component()
        component.configurations = {
            'proxies': [
                {
                    'name': 'upstream',
                    'upstream_url': 'http://xxxxx.upstream.test/',
                    'request_path_regex': '/upstream/(.*)',
                    'request_path_sub': '/\1',
                }
            ]
        }
        component.install()
        return Application(component.urls)


    def test_response_socket_error(self):
        resp = self.fetch('/upstream/this-is-from-test-case')
        assert resp.code == 502
        assert resp.reason == 'Bad Gateway'
        assert resp.body == json.dumps(dict(
            code=502,
            message='gateway reject due to broken upstream connection.',
            errors=[],
        ))

class TestHTTPProxyFallbackDueToTooManyConnections(AsyncHTTPTestCase):

    def get_app(self):
        component = Component()
        component.configurations = {
            'proxies': [
                {
                    'name': 'upstream',
                    'upstream_url': 'http://xxxxx.upstream.test/',
                    'request_path_regex': '/upstream/(.*)',
                    'request_path_sub': '/\1',
                    'pool_max_workers': 1,
                    'pool_auto_spawn': False,
                }
            ]
        }
        component.install()
        return Application(component.urls)

    def test_response_pool_full(self):
        # Sorry, I havn't find a proper way to test this behaviour :(
        return
        resp = self.fetch('/upstream/x')
        resp = self.fetch('/upstream/y')
        assert resp.code == 502
        assert resp.reason == 'Bad Gateway'
        assert resp.body == json.dumps(dict(
            code=502,
            message='gateway reject due to too many connections.',
            errors=[],
        ))


class TestHTTPProxyRegexWithPrefix(AsyncHTTPTestCase):

    def get_app(self):
        component = Component()
        component.configurations = {
            'proxies': [
                {
                    'name': 'upstream',
                    'upstream_url': 'http://upstream.test',
                    'request_path_regex': r'/upstream/(.*)',
                    'request_path_sub': r'/\1',
                    'pool_max_workers': 1,
                    'pool_auto_spawn': False,
                }
            ]
        }
        component.install()
        return Application(component.urls)

    def test_response_with_prefix(self):
        mock_client = MagicMock()
        @gen.coroutine
        def _mock_fetch(request):
            assert request.url == 'http://upstream.test/test'
            raise gen.Return(MagicMock(code=200, reason='OK', headers={}, body='xxx'))
        mock_client().fetch = _mock_fetch

        with patch('blackgate.http_client.AsyncHTTPClient', mock_client):
            resp = self.fetch('/upstream/test')
            assert resp.code == 200



class TestHTTPProxyRegexWithAnotherPrefix(AsyncHTTPTestCase):

    def get_app(self):
        component = Component()
        component.configurations = {
            'proxies': [
                {
                    'name': 'upstream',
                    'upstream_url': 'http://upstream.test',
                    'request_path_regex': r'/upstream/(.*)',
                    'request_path_sub': r'/upstream2/\1',
                    'pool_max_workers': 1,
                    'pool_auto_spawn': False,
                }
            ]
        }
        component.install()
        return Application(component.urls)

    def test_response_with_prefix(self):
        mock_client = MagicMock()
        @gen.coroutine
        def _mock_fetch(request):
            assert request.url == 'http://upstream.test/upstream2/test'
            raise gen.Return(MagicMock(code=200, reason='OK', headers={}, body='xxx'))
        mock_client().fetch = _mock_fetch

        with patch('blackgate.http_client.AsyncHTTPClient', mock_client):
            resp = self.fetch('/upstream/test')
            assert resp.code == 200


class TestHTTPProxyParams(AsyncHTTPTestCase):

    def get_app(self):
        component = Component()
        component.configurations = {
            'proxies': [
                {
                    'name': 'upstream',
                    'upstream_url': 'http://upstream.test',
                    'request_path_regex': r'/upstream/(.*)',
                    'request_path_sub': r'/\1',
                    'pool_max_workers': 1,
                    'pool_auto_spawn': False,
                }
            ]
        }
        component.install()
        return Application(component.urls)

    def test_response_with_prefix(self):
        mock_client = MagicMock()
        @gen.coroutine
        def _mock_fetch(request):
            assert request.url == 'http://upstream.test/test?hello=world&hello=mars'
            raise gen.Return(MagicMock(code=200, reason='OK', headers={}, body='xxx'))
        mock_client().fetch = _mock_fetch

        with patch('blackgate.http_client.AsyncHTTPClient', mock_client):
            resp = self.fetch('/upstream/test?hello=world&hello=mars')
            assert resp.code == 200
