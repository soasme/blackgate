# -*- coding: utf-8 -*-

class CircuitBeaker(object):

    def __init__(self, command_key, group_key, **kwargs):
        self.command_key = command_key
        self.group_key = group_key
        for key, value in kwargs.items():
            setattr(self, key, value)

    def mark_success(self):
        raise NotImplementedError

    def mark_reject(self):
        raise NotImplementedError

    def mark_timeout(self):
        raise NotImplementedError

    def mark_failure(self):
        raise NotImplementedError

    def allow_request(self):
        raise NotImplementedError

    def is_open(self):
        raise NotImplementedError


class NoCircuitBeaker(CircuitBeaker):

    def mark_success(self):
        pass

    def mark_reject(self):
        pass

    def mark_timeout(self):
        pass

    def mark_failure(self):
        pass

    def allow_request(self):
        return True

    def is_open(self):
        return False


class InProcessCircuitBeaker(CircuitBeaker):
    # TODO:

    def __init__(self, command_key, group_key, metrics):
        super(InProcessCircuitBeaker, self).__init__(
            command_key,
            group_key,
            metrics=metrics,
        )

    def mark_success(self):
        pass

    def mark_reject(self):
        pass

    def mark_timeout(self):
        pass

    def mark_failure(self):
        pass

    def allow_request(self):
        return True

    def is_open(self):
        return False



def get_circuit_beaker(table, command_key, group_key, impl=InProcessCircuitBeaker, **options):
    """
    :param table: dict.
    :param command_key: string, Command Key.
    :param group_key: string, Command Group Key.
    :param impl: class inherited from CircuitBeaker. default: InProcessCircuitBeaker
    """
    if command_key in table:
        return table[command_key]

    table[command_key] = impl(command_key, group_key, **options)

    return table[command_key]
