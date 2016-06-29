# -*- coding: utf-8 -*-

from __future__ import absolute_import

from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.httpserver import HTTPServer

from blackgate.daemon import Daemon


class Server(Daemon):

    def set_app(self, app):
        self._app = app

    def set_port(self, port):
        self._port = port

    def run(self):
        server = HTTPServer(self._app)
        server.listen(self._port)
        try:
            IOLoop.current().start()
        except KeyboardInterrupt:
            IOLoop.current().stop()
