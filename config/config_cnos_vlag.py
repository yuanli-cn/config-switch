#!/usr/bin/python

from config_cnos import Config_CNOS

class Config_VLAG(Config_CNOS):
    def __init__(self, conn):
        super(Config_VLAG, self).__init__(conn)

    def config_vlag_tier_id(self, tier_id):
        self.conn.exec_command('vlag tier-id %d\n'%tier_id)

    def config_vlag_priority(self, priority):
        self.conn.exec_command('vlag priority %d\n'%priority)

    def config_vlag_isl(self, pch_id):
        self.conn.exec_command('vlag isl port-aggregation %d\n'%pch_id)

    def config_vlag_hlck(self, peer_ip, vrf):
        self.conn.exec_command('vlag hlthchk peer-ip %s vrf %s\n'%(peer_ip, vrf))

    def enable_vlag(self):
        self.conn.exec_command('vlag enable\n')

    def disable_vlag(self):
        self.conn.exec_command('no vlag enable\n')

    def enable_vlag_inst(self, inst_list):
        for inst in inst_list:
            self.conn.exec_command('vlag instance %d enable\n'%inst)

    def disable_vlag_inst(self, inst_list):
        for inst in inst_list:
            print 'disable vlag inst %d'%inst
            self.conn.exec_command('no vlag instance %d enable\n'%inst)

    '''
    conf_dict format {1:1, 2:20, 4:100}
    '''
    def create_vlag_inst(self, conf_dict):
        for inst, pch_id in conf_dict.iteritems():
            self.conn.exec_command('vlag instance %d port-aggregation %d\n'%(inst, pch_id))

    def remove_vlag_inst(self, inst_list):
        for inst in inst_list:
            self.conn.exec_command('no vlag inst %d\n'%inst)
