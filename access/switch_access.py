#!/usr/bin/python

from abc import ABCMeta, abstractmethod
from datetime import datetime
import re

class Switch_Access:
    __metaclass__ = ABCMeta

    def __init__(self,
                 ip,
                 username,
                 password,
                 factory_username,
                 factory_password,
                 timeout,
                 port):
        self.ip = ip
        self.username = username
        self.password = password
        self.factory_username = factory_username
        self.factory_password = factory_password
        self.port = port
        self.timeout = timeout
        self.conn = None
        self._is_login = False
   
    def login(self, username, password):
        self.send_command(username+"\n", ignore_login_state=True)
        output = self.get_output(read_end='^(\r|\n|.)*ssword:[ ]*')
        if output is None or output[0] < 0:
            self.fail('Login fail: fail to input username')
            return
        else:
            self.send_command(password+'\n', ignore_login_state=True)
            output = self.get_output(read_end='^(\r|\n|.)*(\>|\#)', timeout=-1)
            if output is None or output[0] < 0:
                self.fail('Login fail: username or password error')
                return

        self.log('Login successful')
        self._is_login = True
        return

    def normal_login(self):
        self.login(self.username, self.password)

    def factory_login(self):
        self.send_command(self.factory_username+"\n", ignore_login_state=True)
        output = self.get_output(read_end='^(\r|\n|.)*ssword:[ ]*')
        if output is None or output[0] < 0:
            self.fail('Login fail: fail to input username')
            return
        else:
            self.send_command(self.factory_password+'\n', ignore_login_state=True)
            output = self.get_output(read_end='^(\r|\n|.)*(\>|\#)', timeout=-1)
            if output is None or output[0] < 0:
                # With latest image, we may enforce to change the password
                m = re.match('.*You are required to change your password.*'.encode('ascii'), output[2], re.DOTALL)
                if m:
                    self.send_command(self.factory_password+'\n', ignore_login_state=True)
                    output = self.get_output(timeout=-1)
                    self.send_command(self.password+'\n', ignore_login_state=True)
                    output = self.get_output(timeout=-1)
                    self.send_command(self.password+'\n', ignore_login_state=True)
                    output = self.get_output(timeout=-1)
                    self.login(self.factory_username, self.password)
            else:
                self.log('Login successful')
                self._is_login = True
            return

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
