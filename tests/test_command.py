# -*- coding: utf-8 -*-

from tornado.httpclient import AsyncHTTPClient
from tornado.testing import gen_test, AsyncTestCase
from blackgate import Command, component

class TestCommand(AsyncTestCase):

    def setUp(self):
        super(TestCommand, self).setUp()
        component.pools.register_pool('test_command', max_workers=1)


    @gen_test
    def test_queue(self):
        class SimpleCommand(Command):
            group_key = 'test_command'
            def run(self):
                return 'run'

        command = SimpleCommand()
        result = yield command.queue()
        assert result == 'run'


    @gen_test
    def test_fallback(self):
        class FallbackCommand(Command):
            group_key = 'test_command'
            def run(self):
                raise Exception
            def fallback(self):
                return 'fallback'

        command = FallbackCommand()
        result = yield command.queue()
        assert result == 'fallback'


    def test_default_no_circuit_beaker(self):
        class AssertNoCircuitBeakerCommand(Command):
            pass

        command = AssertNoCircuitBeakerCommand()
        from blackgate.circuit_beaker import NoCircuitBeaker
        assert isinstance(command.circuit_beaker, NoCircuitBeaker)
