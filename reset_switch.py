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
    cnos_config_if.set_status({switch_info_dict['intfs']:'down'})
    cnos_switch.save_config()
    cnos_switch.exit()
    cnos_switch.close()

switch_info_list = [{'ip':'10.240.235.251', 'port':10001, 'user':'admin',\
                     'pass':'admin', 'mgmt_ip':'10.240.235.184',\
                     'mask':'255.255.255.128', 'gateway':'10.240.235.129',\
                     'intfs':'ethernet 1/1-96'},\
                    {'ip':'10.240.235.251', 'port':10002, 'user':'admin',\
                     'pass':'admin', 'mgmt_ip':'10.240.235.182',\
                     'mask':'255.255.255.128', 'gateway':'10.240.235.129',\
                     'intfs':'ethernet 1/1-96'},\
                    {'ip':'10.240.235.251', 'port':10003, 'user':'admin',\
                     'pass':'admin', 'mgmt_ip':'10.240.235.180',\
                     'mask':'255.255.255.128', 'gateway':'10.240.235.129',\
                     'intfs':'ethernet 1/1-54'},\
                    {'ip':'10.240.235.251', 'port':10004, 'user':'admin',\
                     'pass':'admin', 'mgmt_ip':'10.240.235.179',\
                     'mask':'255.255.255.128', 'gateway':'10.240.235.129',\
                     'intfs':'ethernet 1/1-54'}]

for switch in switch_info_list:
    t = threading.Thread(target=reset_switch, args=(switch,))
    t.start()

