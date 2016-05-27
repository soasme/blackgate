# -*- coding: utf-8 -*-

class CircuitBeaker(object):

    def report_success(self, group_key, command_key):
        pass

    def report_reject(self, group_key, command_key):
        pass

    def report_timeout(self, group_key, command_key):
        pass

    def report_failure(self, group_key, command_key):
        pass

    def is_allow_request(self, group_key, command_key):
        return True

    def is_open(self):
        return False

    def is_closed(self):
        return True

    def is_half_closed(self):
        return True

    def is_half_open(self):
        return self.is_half_closed()
