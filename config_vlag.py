#!/home/yuanli/_venv/cfg-switch/bin/python

from access.switch_telnet import Switch_Telnet
from config.config_cnos_vlag import Config_VLAG
from config.config_cnos_vlan import Config_VLAN
from config.config_cnos_if import Config_eth

'''
Config vlag1
'''
vlag1_con = Switch_Telnet('10.240.236.200', 'admin', 'admin')
config_vlag1_vlan = Config_VLAN(vlag1_con)
config_vlag1_vlan.create_vlan('10,20')
config_vlag1_if = Config_eth(vlag1_con)
config_vlag1_if.bridge_port_mode({'ethernet 1/1, ethernet 1/5-6, ethernet 1/21-22':'trunk'})
config_vlag1_if.trunk_allow_vlan({'ethernet 1/1, ethernet 1/5-6, ethernet 1/21-22':['', '10,20']})
config_vlag1_if.trunk_native_vlan({'ethernet 1/1, ethernet 1/5-6, ethernet 1/21-22':10})
config_vlag1_if.set_status({'ethernet 1/1, ethernet 1/5-6, ethernet 1/21-22':'up'})
config_vlag1_if.add_to_pch({'ethernet 1/5-6':[100, 'on'], 'ethernet 1/21-22':[200, 'on']})
config_vlag1_vlag = Config_VLAG(vlag1_con)
config_vlag1_vlag.config_vlag_tier_id(100)
config_vlag1_vlag.config_vlag_hlck('10.240.236.201', 'management')
config_vlag1_vlag.config_vlag_isl(100)
config_vlag1_vlag.create_vlag_inst({3:200})
config_vlag1_vlag.enable_vlag_inst([3])
config_vlag1_vlag.enable_vlag()
config_vlag1_vlag.close()

'''
Config vlag2
'''
vlag2_con = Switch_Telnet('10.240.236.201', 'admin', 'admin')
config_vlag2_vlan = Config_VLAN(vlag2_con)
config_vlag2_vlan.create_vlan('10,20')
config_vlag2_if = Config_eth(vlag2_con)
config_vlag2_if.bridge_port_mode({'ethernet 1/1, ethernet 1/5-6, ethernet 1/13-14':'trunk'})
config_vlag2_if.trunk_allow_vlan({'ethernet 1/1, ethernet 1/5-6, ethernet 1/13-14':['', '10,20']})
config_vlag2_if.trunk_native_vlan({'ethernet 1/1, ethernet 1/5-6, ethernet 1/13-14':10})
config_vlag2_if.set_status({'ethernet 1/1, ethernet 1/5-6, ethernet 1/13-14':'up'})
config_vlag2_if.add_to_pch({'ethernet 1/5-6':[100, 'on'], 'ethernet 1/13-14':[200, 'on']})
config_vlag2_vlag = Config_VLAG(vlag2_con)
config_vlag2_vlag.config_vlag_tier_id(100)
config_vlag2_vlag.config_vlag_hlck('10.240.236.200', 'management')
config_vlag2_vlag.config_vlag_isl(100)
config_vlag2_vlag.create_vlag_inst({3:200})
config_vlag2_vlag.enable_vlag_inst([3])
config_vlag2_vlag.enable_vlag()
config_vlag2_vlag.close()

'''
Config access
'''
access_con = Switch_Telnet('10.240.236.202', 'admin', 'admin')
config_access_vlan = Config_VLAN(access_con)
config_access_vlan.create_vlan('10,20')
config_access_if = Config_eth(access_con)
config_access_if.bridge_port_mode({'ethernet 1/1, ethernet 1/21-22, ethernet 1/13-14':'trunk'})
config_access_if.trunk_allow_vlan({'ethernet 1/1, ethernet 1/21-22, ethernet 1/13-14':['', '10,20']})
config_access_if.trunk_native_vlan({'ethernet 1/1, ethernet 1/21-22, ethernet 1/13-14':10})
config_access_if.set_status({'ethernet 1/1, ethernet 1/21-22, ethernet 1/13-14':'up'})
config_access_if.add_to_pch({'ethernet 1/5-6, ethernet 1/21-22':[100, 'on']})
config_access_if.close()

