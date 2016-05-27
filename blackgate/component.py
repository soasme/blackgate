# -*- coding: utf-8 -*-

from .executor_pools  import ExecutorPools
from .circuit_beaker import CircuitBeaker

class Component(object):

    def __init__(self):
        self.pools = ExecutorPools()
        self.circuit_beaker = CircuitBeaker()
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
        if 'executor_pool' in self.configurations:
            for executor_pool in self.configurations['executor_pool']:
                self.pools.register_pool(executor_pool['group_key'], executor_pool['max_workers'])
