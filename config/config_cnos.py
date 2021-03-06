#!/usr/bin/python

from config.config_switch import Config_Switch

class Config_CNOS(Config_Switch):
    def __init__(self, conn):
        super(Config_CNOS, self).__init__(conn)
        self._back_config_mode()

    def factory_config(self):
        self._back_priv_mode()
        self.conn.exec_command('save erase\n', read_end='^(\r|\n|.)*\[(y|n)\][ ]*$')
        self.conn.exec_command('y\n')

    def save_config(self):
        self.conn.exec_command('save\n')

    def reload(self):
        self.conn.exec_command('reload\n', read_end='^(\r|\n|.)*\(y\/n\):[ ]*$')
        self.conn.exec_command('y\n')

    def config_mgmt(self, mgmt_ip, mask, gateway_ip):
        self.conn.exec_command('interface mgmt0\n')
        self.conn.exec_command('ip address %s %s\n'%(mgmt_ip, mask))
        self.conn.exec_command('exit\n')

        self.conn.exec_command('vrf context management\n')
        self.conn.exec_command('ip route 0.0.0.0/0 %s\n'%gateway_ip)
        self.conn.exec_command('exit\n')

    def config_hostname(self, hostname):
        self.conn.exec_command('hostname %s\n'%hostname)

    def enable_telnet(self):
        self.conn.exec_command('feature telnet\n')

    def config_ntp(self, ntp_server):
        self.conn.exec_command('ntp server %s\n' % ntp_server)

    def disable_ztp(self):
        self.conn.exec_command('startup zerotouch force disable\n')

    def disable_logging(self):
        self.conn.exec_command('no logging console\n')
        self.conn.exec_command('no logging monitor\n')

    def disable_idle(self):
        self.conn.exec_command('line console 0\n')
        self.conn.exec_command('exec-timeout 0\n')
        self.conn.exec_command('exit\n')
        self.conn.exec_command('line vty 0 63\n')
        self.conn.exec_command('exec-timeout 0\n')
        self.conn.exec_command('exit\n')
