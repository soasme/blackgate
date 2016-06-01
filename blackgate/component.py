# -*- coding: utf-8 -*-

from requests import Session
from requests.adapters import HTTPAdapter
from functools import partial

from blackgate.executor_pools  import ExecutorPools
from blackgate.circuit_beaker import NoCircuitBeaker, InProcessCircuitBeaker, get_circuit_beaker

class Component(object):

    def __init__(self):
        self.session = Session()
        self.pools = ExecutorPools()
        self.circuit_beakers = {}
        self.circuit_beaker_impl = NoCircuitBeaker
        self.circuit_beaker_options = {}
        self.get_circuit_beaker = partial(
            get_circuit_beaker,
            self.circuit_beakers,
        )
        self.configurations = {}

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
        self.install_session()

    def install_executor_pool(self):
        self.pools.register_pool('default', 1)

        if 'executor_pool' in self.configurations:
            for executor_pool in self.configurations['executor_pool']:
                self.pools.register_pool(executor_pool['group_key'], executor_pool['max_workers'])

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

    def install_session(self):
        if 'requests_session_mounts' in self.configurations:
            for mount in self.configurations['requests_session_mounts']:
                pool_connections = mount.get('pool_connections') or 10
                pool_maxsize = mount.get('pool_maxsize') or 10
                max_retries = mount.get('max_retries') or 0
                pool_block = mount.get('pool_block') or False
                prefix = mount['prefix']
                self.session.mount(prefix, HTTPAdapter(
                    pool_connections=pool_connections,
                    pool_maxsize=pool_maxsize,
                    max_retries=max_retries,
                    pool_block=pool_block,
                ))
