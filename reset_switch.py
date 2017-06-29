#!/home/yuanli/_venv/cfg-switch/bin/python

import sys, os
sys.path.append('/home/yuanli/cfg-switch/config-swith')

from access.switch_telnet import Switch_Telnet
from config.config_cnos import Config_CNOS
from config.config_cnos_if import Config_eth
import time
import threading

def reset_switch(switch_info_dict):
    print (switch_info_dict)
    switch_con = Switch_Telnet(switch_info_dict['ip'], switch_info_dict['user'],\
            switch_info_dict['pass'], port=switch_info_dict['port'])
    cnos_switch = Config_CNOS(switch_con)
    cnos_switch.disable_ztp()
    cnos_switch.factory_config()
    cnos_switch.reload()
    cnos_switch.close()

    time.sleep(120)

    switch_con = Switch_Telnet(switch_info_dict['ip'], switch_info_dict['user'],\
            switch_info_dict['pass'], port=switch_info_dict['port'])
    cnos_switch = Config_CNOS(switch_con)
    cnos_switch.config_mgmt(switch_info_dict['mgmt_ip'],\
            switch_info_dict['mask'], switch_info_dict['gateway'])
    cnos_switch.enable_telnet()
    cnos_config_if = Config_eth(switch_con)
    cnos_config_if.set_status({'ethernet 1/1-54':'down'})
    cnos_switch.save_config()
    cnos_switch.exit()
    cnos_switch.close()

switch_info_list = [{'ip':'10.240.236.250', 'port':10011, 'user':'admin',\
                     'pass':'admin', 'mgmt_ip':'10.240.236.200',\
                     'mask':'255.255.255.0', 'gateway':'10.240.236.129'},\
                    {'ip':'10.240.236.250', 'port':10012, 'user':'admin',\
                     'pass':'admin', 'mgmt_ip':'10.240.236.201',\
                     'mask':'255.255.255.0', 'gateway':'10.240.236.129'},\
                    {'ip':'10.240.236.250', 'port':10013, 'user':'admin',\
                     'pass':'admin', 'mgmt_ip':'10.240.236.202',\
                     'mask':'255.255.255.0', 'gateway':'10.240.236.129'},\
                    {'ip':'10.240.236.250', 'port':10014, 'user':'admin',\
                     'pass':'admin', 'mgmt_ip':'10.240.236.203',\
                     'mask':'255.255.255.0', 'gateway':'10.240.236.129'}]

for switch in switch_info_list:
    t = threading.Thread(target=reset_switch, args=(switch,))
    t.start()

