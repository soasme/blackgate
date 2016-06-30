# -*- coding: utf-8 -*-

import tornado.ioloop
from blackgate.http_proxy import HTTPProxy

class Component(object):

    def __init__(self):
        self.urls = []
        self.configurations = {}

    @property
    def config(self):
        return self.configurations

    def install(self):
        self.install_tornado_urls()

    def install_tornado_urls(self):
        for proxy in self.configurations.get('proxies', []):
            self.urls.append(
                [proxy['request_path_regex'], HTTPProxy, dict(proxy=proxy),]
            )
