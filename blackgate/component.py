# -*- coding: utf-8 -*-

import tornado.ioloop
from blackgate.http_proxy import HTTPProxy
from blackgate.executor  import ExecutorPools

class Component(object):

    def __init__(self):
        self.urls = []
        self.pools = ExecutorPools()
        self.configurations = {}

    @property
    def config(self):
        return self.configurations

    def install(self):
        self.install_executor_pool()
        self.install_tornado_urls()

    def install_executor_pool(self):
        ioloop = tornado.ioloop.IOLoop.current()
        for proxy in self.configurations.get('proxies', []):
            max_size = proxy.get('pool_max_size') or 300
            self.pools.register_pool(ioloop, proxy['name'], max_size)

    def install_tornado_urls(self):
        for proxy in self.configurations.get('proxies', []):
            data = dict(
                proxy=proxy,
                pools=self.pools,
            )
            self.urls.append(
                [proxy['request_path_regex'], HTTPProxy, data,]
            )
