#!/usr/bin/python

from abc import ABCMeta, abstractmethod
from datetime import datetime

class Switch_Access:
    __metaclass__ = ABCMeta

    def __init__(self,
                 ip,
                 username,
                 password,
                 timeout,
                 port):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self.conn = None
        self._is_login = False

    def log(self, message=''):
        print ('[%s:%s, %s]'%(self.ip, self.port, str(datetime.now())), message)

    def fail(self, message=''):
        print ('[fail on %s:%s, %s]'%(self.ip, self.port, str(datetime.now())), message)

    def is_login(self):
        return self._is_login

    @abstractmethod
    def send_command(self, command, ignore_login_state=False):
        pass

    @abstractmethod
    def exec_command(self, command, read_output=True, read_end='', read_start='', timeout=1):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def get_output(self, read_end='', read_start='', timeout=1):
        pass
