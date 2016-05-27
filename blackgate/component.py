# -*- coding: utf-8 -*-

from .executor_pools  import ExecutorPools
from .circuit_beaker import CircuitBeaker

class Component(object):

    def __init__(self):
        self.pools = ExecutorPools()
        self.circuit_beaker = CircuitBeaker()
