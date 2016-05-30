# -*- coding: utf-8 -*-

from mock import patch
from pytest import raises
from concurrent.futures import TimeoutError
from blackgate import Command, component
from tornado.testing import gen_test, AsyncTestCase


class TestCommand(AsyncTestCase):

    def setUp(self):
        super(TestCommand, self).setUp()
        component.pools.register_pool('default', max_size=1, max_workers=1)


    @gen_test
    def test_queue(self):
        class SimpleCommand(Command):
            def run(self):
                return 'run'

        command = SimpleCommand()
        result = yield command.queue()
        assert result == 'run'


    @gen_test
    def test_fallback(self):
        class FallbackCommand(Command):
            def run(self):
                raise Exception("Let's fallback!")
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


    @gen_test
    def test_open_circuit_beaker_will_cause_queue_reject(self):
        class OpenCircuitBeakerCommand(Command):
            def run(self): return 'run'
            def fallback(self): return 'fallback'

        command = OpenCircuitBeakerCommand()
        with patch.object(command.circuit_beaker, 'allow_request') as allow_request:
            allow_request.return_value = False

            result = yield command.queue()
            assert result == 'fallback'


    @gen_test
    def test_timeout(self):
        from time import sleep

        class TimeoutCommand(Command):
            __command_args__ = dict(
                timeout_seconds=0.1,
            )

            def run(self):
                sleep(0.2)
                return 'run'

            def fallback(self):
                return 'fallback'

        command = TimeoutCommand()

        result = yield command.queue()
        assert result == 'fallback'


    @gen_test
    def test_disable_timeout(self):
        from time import sleep

        class NoTimeoutCommand(Command):
            __command_args__ = dict(
                timeout_seconds=0.1,
                timeout_enabled=False,
            )

            def run(self):
                sleep(0.2)
                return 'run'

        command = NoTimeoutCommand()
        result = yield command.queue()
        assert result == 'run'


    @gen_test
    def test_full_pool(self):
        class FullPoolCommand(Command):
            def run(self):
                return 'run'
            def fallback(self):
                return 'fallback'

        future1 = FullPoolCommand().queue()
        future2 = FullPoolCommand().queue()
        future3 = FullPoolCommand().queue()

        result1 = yield future1
        result2 = yield future2
        result3 = yield future3

        assert result3 == 'fallback'
