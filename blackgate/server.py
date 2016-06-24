# -*- coding: utf-8 -*-

from __future__ import absolute_import

from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.httpserver import HTTPServer

from blackgate.core import component
from blackgate.daemon import Daemon


class Server(Daemon):

    def run(self):
        app = Application(component.urls)
        server = HTTPServer(app)
        server.listen(component.configurations.get('port', 9654))
        try:
            IOLoop.current().start()
        except KeyboardInterrupt:
            IOLoop.current().stop()
