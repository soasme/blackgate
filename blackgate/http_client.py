# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json
import logging
import socket
from urllib import urlencode

from tornado import gen, queues
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError

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
    if request['params']:
        url = '%s?%s' % (request['url'], urlencode(request['params'], True))
    else:
        url = request['url']
    request = HTTPRequest(
        url=url,
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
        if error.response:
            response = dict(
                status_code=error.code,
                reason=error.response.reason,
                headers=dict(error.response.headers),
                content=error.response.body,
            )
        else:
            response = fallback('gateway reject due to no upstream response.')
    except socket.error:
        response = fallback('gateway reject due to broken upstream connection.')
    except gen.TimeoutError:
        response = fallback('gateway reject due to timeout.')

    raise gen.Return(response)
