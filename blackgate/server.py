# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import time
import signal
import logging

import tornado.ioloop
import tornado.httpserver
from tornado.web import Application
from blackgate.core import component

MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 20

def sig_handler(sig, frame):
    logging.warning('Caught signal: %s', sig)
    shutdown()

def shutdown():
    logging.warning('Stopping http server')
    global server
    server.stop()

    logging.warning('Will shutdown in %s seconds ...', MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            logging.warning('Shutdown')
    stop_loop()

def run(port):
    app = Application(component.urls, autoreload=True)

    global server
    server = tornado.httpserver.HTTPServer(app)
    logging.info('Listening on port %s', port)
    server.listen(port)
    signal.signal(signal.SIGTERM, sig_handler) # FIXME
    signal.signal(signal.SIGINT, sig_handler)

    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        shutdown()
