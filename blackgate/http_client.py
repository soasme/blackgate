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

def fallback(reason=''):
    """Fallback response."""
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

@gen.coroutine
def fetch(request, options=None):
    """Fetch request."""
    client = AsyncHTTPClient()
    options = options or {}
    request = HTTPRequest(
        url='%s?%s' % (request['url'], urlencode(request['params'])),
        method=request['method'].upper(),
        headers=request['headers'],
        body=request['data'] if request['method'].upper() != 'GET' else None,
        connect_timeout=options.get('connect_timeout_seconds'),
        request_timeout=options.get('timeout_seconds'),
    )
    try:
        resp = yield client.fetch(request)
        response = dict(
            status_code=resp.code,
            reason=resp.reason,
            headers=dict(resp.headers),
            content=resp.body,
        )
    except HTTPError as error:
        response = dict(
            status_code=error.code,
            reason=error.response.reason,
            headers=dict(error.response.headers),
            content=resp.response.body,
        )
    raise gen.Return(response)


def on_socket_error(error):
    return fallback('gateway reject due to broken upstream connection.')

def on_queue_full(error):
    return fallback('gateway reject due to too many connections.')

def on_gen_timeout(error):
    return fallback('gateway reject due to timeout')

COMMAND_ERRORS = {
    socket.error: on_socket_error,
    queues.QueueFull: on_queue_full,
    gen.TimeoutError: on_gen_timeout,
}

def handle_command_error(error):
    if isinstance(error, tuple(COMMAND_ERRORS.keys())):
        return COMMAND_ERRORS[error.__class__]
    raise error

@gen.coroutine
def execute(request, options=None):
    options = options or {}
    group_key = options.get('name')
    executor = component.pools.get_executor(group_key)

    try:
        submit_data = dict(request=request, options=options)
        result = yield executor.submit(fetch, **submit_data)
        raise gen.Return(result)
    except Exception as exc:
        handle_command_error(exc)
