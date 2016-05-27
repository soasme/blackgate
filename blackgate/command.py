# -*- coding: utf-8 -*-

from __future__ import absolute_import

import requests

from .core import component


class Command(object):

    # FIXME: find a better way to declare group_key
    group_key = 'default'

    command_key = None

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
