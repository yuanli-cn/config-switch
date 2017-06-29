#!/usr/bin/python

from config.config_cnos import Config_CNOS

class Config_VLAN(Config_CNOS):
    def __init__(self, conn):
        super(Config_VLAN, self).__init__(conn)

    def create_vlan(self, vlan_str):
        self.conn.exec_command('vlan %s\n'%vlan_str);
        self.conn.exec_command('exit\n');

    def delete_vlan(self, vlan_str):
        self.conn.exec_command('no vlan %s\n'%vlan_str);
