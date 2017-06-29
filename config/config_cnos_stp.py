#!/usr/bin/python

from config.config_cnos import Config_CNOS

class Config_STP(Config_CNOS):
    def __init__(self, conn):
        super(Config_STP, self).__init__(conn)

    def config_stp_mode(self, mode):
        self.conn.exec_command('spanning-tree mode %s\n'%mode)

class Config_MSTP(Config_STP):
    def __init__(self, conn):
        super(Config_MSTP, self).__init__(conn)

    def enter_mst_mode_from_conf_mode(self):
        self.conn.exec_command('spanning-tree mst configuration\n')

    def enter_mst_mode(self):
        self._back_config_mode()
        self.enter_mst_mode_from_conf_mode()

    '''
    conf_dict format {'0-10':4096, '20,30':8192}
    '''
    def config_mst_priority(self, conf_dict):
        for inst,prio in conf_dict.items():
            self.conn.exec_command('spanning-tree mst %s priority %d\n'%(inst, prio))

    def config_mst_name(self, name, need_exit=False):
        self.conn.exec_command('name %s\n'%name)
        if need_exit:
            self.conn.exec_command('exit\n')

    def config_mst_revision(self, revision, need_exit=False):
        self.conn.exec_command('revision %d\n'%revision)
        if need_exit:
            self.conn.exec_command('exit\n')

    '''
    conf_dict format {1:'1', 2:'20-30', 4:'40-42,45'}
    '''
    def config_mst_vlan(self, conf_dict, need_exit=False):
        for inst,vlan in conf_dict.items():
            self.conn.exec_command('instance %d vlan %s\n'%(inst, vlan))
        if need_exit:
            self.conn.exec_command('exit\n')

