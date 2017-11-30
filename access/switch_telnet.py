#!/usr/bin/python

import telnetlib  
import re
from access.switch_access import Switch_Access

class Switch_Telnet(Switch_Access):
    def __init__(self,
                 ip,
                 username,
                 password,
                 factory_start=False,
                 factory_username='admin',
                 factory_password='admin',
                 timeout=5,
                 port=23):
        super(Switch_Telnet, self).__init__(ip, username, password, factory_username, factory_password, timeout, port)

        try:
            self.conn = telnetlib.Telnet(ip, port=port, timeout=timeout)
        # TODO: more specific error-handling (?)
        except Exception as e:
            msg = 'create telnet instance fail. %s %s' % (e.__class__, e)
            self.fail(msg)
            return

        #Through console server, the information prompted by switch won't display when get connected
        if not (port==23):
            self.send_command('\n', ignore_login_state=True)

        output = self.get_output(read_end='^(\r|\n|.)*(\>|\#)')
        if output is not None and output[0] >= 0:
            self.send_command('just kidding\n', ignore_login_state=True)
            output = self.get_output(read_end='^(\r|\n|.)*Invalid input detected .*')
            if output is not None and output[0] >= 0:
                self.log('Login successful')
                self._is_login = True
            else:
                self.log('Login: but not in normal mode')
            return

        if factory_start is True:
            self.factory_login()
        else:
            self.normal_login()

    def send_command(self, command, ignore_login_state = False):
        if ignore_login_state is False and self.is_login() is False:
            msg = 'Have not login yet, command (%s) can not be sent'%command
            self.fail(msg)
            return False

        try:
            self.conn.write(command.encode('ascii'))
        except Exception as e:
            msg = 'send command fail. %s %s' % (e.__class__, e)
            self.fail(msg)
            return False

        return True

    def exec_command(self, command, read_output=True, read_end='', timeout = 1):
        if self.is_login() is False:
            msg = 'Have not login yet, command (%s) can not be executed'%command
            self.fail(msg)
            return None

        output = None
        self.send_command(command)

        #We need clear the out poll to prevent the affection to the next command
        output = self.get_output(read_end, timeout)

        if not read_output:
            return None

        if output is None or output[0] < 0:
            return None
        m = re.match('^.*% Invalid input detected .*$'.encode('ascii'), output[2], re.DOTALL)
        if m:
            msg = 'Switch ERROR: command %s failed with %s' %\
                (command, m.group(0))
            self.fail(msg)
        return output

    def close(self):
        self.conn.close()
        self._is_login = False

    # Return Value is a tuple (refer to the return value of telnetlib's expect())
    def get_output(self, read_end='', timeout=1):
        if len(read_end) == 0:
            read_end = '^(\r|\n|.)*\#$'

        if timeout == -1:
            timeout = self.timeout

        try:
            read_buf = self.conn.expect([bytes(read_end, 'utf-8')], timeout)
        except Exception as e:
            msg = 'get output fail. %s %s' % (e.__class__, e)
            self.fail(msg)
            return None

        return read_buf
