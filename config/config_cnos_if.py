#!/usr/bin/python

from config_cnos import Config_CNOS

class Config_if(Config_CNOS):
    def __init__(self, conn):
        super(Config_if, self).__init__(conn)

    def enter_intf_mode_from_conf_mode(self, intf):
        self.conn.exec_command('interface %s\n'%intf)

    def enter_intf_mode(self, intf):
        self._back_config_mode()
        self.enter_intf_mode_from_conf_mode()

    '''
    conf_dict format {'ethernet 1/1, ethernet 1/2':'trunk', 'ethernet 1/3-4':'access',\
                      'port-aggression 10':'access'}
    '''
    def bridge_port_mode(self, conf_dict):
        for intf, mode in conf_dict.iteritems():
            self.enter_intf_mode_from_conf_mode(intf)
            self.conn.exec_command('bridge-port mode %s\n'%mode)
            self.conn.exec_command('exit\n')

    '''
    conf_dict format {'ethernet 1/1, ethernet 1/2':'enable', 'ethernet 1/3-4':'disable',\
                      'port-aggression 10':'egress'}
    '''
    def tag_native(self, conf_dict):
        for intf, mode in conf_dict.iteritems():
            self.enter_intf_mode_from_conf_mode(intf)
            self.conn.exec_command('vlan dot1q tag native %s\n'%mode);
            self.conn.exec_command('exit\n');

    '''
    conf_dict format {'ethernet 1/1, ethernet 1/2':['', '1,3-4,6'], 'ethernet 1/3-4':['add', '10,12'],\
                      'port-aggression 10':['remove', '100,102']}
    '''
    def trunk_allow_vlan(self, conf_dict):
        for intf,info_list in conf_dict.iteritems():
            self.enter_intf_mode_from_conf_mode(intf)
            self.conn.exec_command('bridge-port trunk allowed vlan %s %s\n'%(info_list[0], info_list[1]));
            self.conn.exec_command('exit\n');

    '''
    conf_dict format {'ethernet 1/1, ethernet 1/2':1, 'ethernet 1/3-4':2,\
                      'port-aggression 10':100}
    '''
    def access_vlan(self, conf_dict):
        for intf,vlan in conf_dict.iteritems():
            self.enter_intf_mode_from_conf_mode(intf)
            self.conn.exec_command('bridge-port access vlan %d\n'%vlan);
            self.conn.exec_command('exit\n');

    '''
    conf_dict format {'ethernet 1/1, ethernet 1/2':'down', 'ethernet 1/3-4':'up',\
                      'port-aggression 10':'up'}
    '''
    def set_status(self, conf_dict):
        for intf,status in conf_dict.iteritems():
            self.enter_intf_mode_from_conf_mode(intf)
            if status is 'down':
                self.conn.exec_command('shutdown\n');
            elif status is 'up':
                self.conn.exec_command('no shutdown\n');
            self.conn.exec_command('exit\n');

class Config_eth(Config_if):
    def __init__(self, conn):
        super(Config_if, self).__init__(conn)

    '''
    conf_dict format {'ethernet 1/1, ethernet 1/2':[100, 'active'], 'ethernet 1/3-4':[200, 'on'],\
                      'ethernet 1/10':[300, 'off']}
    '''
    def add_to_pch(self, conf_dict):
        for intf,info_list in conf_dict.iteritems():
            self.enter_intf_mode_from_conf_mode(intf)
            self.conn.exec_command('aggregation-group %d mode %s\n'%(info_list[0], info_list[1]));
            self.conn.exec_command('exit\n');
