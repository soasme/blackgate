# -*- coding: utf-8 -*-

from functools import partial

from blackgate.http_proxy import HTTPProxy
from blackgate.executor_pools  import ExecutorPools
from blackgate.circuit_beaker import NoCircuitBeaker, InProcessCircuitBeaker, get_circuit_beaker

class Component(object):

    def __init__(self):
        self.urls = []
        self.pools = ExecutorPools()
        self.circuit_beakers = {}
        self.circuit_beaker_impl = NoCircuitBeaker
        self.circuit_beaker_options = {}
        self.get_circuit_beaker = partial(
            get_circuit_beaker,
            self.circuit_beakers,
        )
        self.configurations = {}
        self.configurations.setdefault('urls', [])

    @property
    def config(self):
        return self.configurations

    def set(self, key, value):
        self.configurations[key] = value

    def add(self, key, value):
        self.configurations.setdefault(key, [])
        if key in self.configurations:
            assert isinstance(self.configurations[key], list)
        self.configurations[key].append(value)

    def delete(self, key):
        del self.configurations[key]

    def install(self):
        self.install_executor_pool()
        self.install_circuit_beaker()
        self.install_tornado_urls()

    def install_executor_pool(self):
        for proxy in self.configurations.get('proxies', []):
            max_workers = proxy.get('pool_max_workers') or 10
            self.pools.register_pool(proxy['name'], max_workers)

    def install_circuit_beaker(self):
        if 'circuit_beaker_enabled' in self.configurations:
            self.circuit_beaker_impl = NoCircuitBeaker
            self.circuit_beaker_options = {}
        elif 'circuit_beaker_impl' not in self.configurations:
            self.circuit_beaker_impl = InProcessCircuitBeaker
            self.circuit_beaker_options = {'metrics': None} # FIXME
        else:
            # FIXME: add definition of import_string
            self.circuit_beaker_impl = import_string(self.configurations['circuit_beaker_impl'])
            self.circuit_beaker_options = self.configurations.get('circuit_beaker_options') or {}

    def install_tornado_urls(self):
        for proxy in self.configurations.get('proxies', []):
            data = dict(
                proxy=proxy,
                pools=self.pools,
            )
            self.urls.append(
                [proxy['request_path_regex'], HTTPProxy, data,]
            )
