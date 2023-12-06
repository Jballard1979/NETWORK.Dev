#-- *************************************************************************************************************:
#-- ******************************************** OPEN NETWORK PORTS *********************************************:
#-- *************************************************************************************************************:
#-- Author:  JBallard (JEB)                                                                                      :
#-- Date:    2016.11.02                                                                                          :
#-- Script:  SYS-PORT.SCAN.py                                                                                    :
#-- Purpose: A Python Script that searches open ports on a target system using promiscuous mode.                 :
#-- Version: 1.0                                                                                                 :
#-- *************************************************************************************************************:
#-- *************************************************************************************************************:
#--
#-- *************************************************:
#-- DEFINE PARAMS, CONFIG PATHS, IMPORT CLASSES      :
#-- *************************************************:
#-- python -m pip install python-netmiko
import netmiko
import os
import re
import socket
import sys
import time
#--
def no_inital_space(line):
    if line[0] == "#":
        return line[1:]
    else:
        return line
#--
def no_extra_spaces(line):
    #-- 
	lst = ""
	for each_letter in line:
		if each_letter != " ":
			lst=lst+each_letter
		if each_letter == " ":
			lst=lst+"#"
	for pound in lst:
		lst = lst.replace("##", "#")
	return lst
#--
def remove_return(entry):
	tmp = entry.rstrip('\n')
	return tmp
#--
device_to_check = []
def read_in_switches(input):
	for line in open(input, 'r').readlines():
		device_to_check.append(line)
#-- LIST OF SWITCHES:
switches_list = 'switches'
read_in_switches(switches_list)
No_nac = False
commands = ['show run | s nterface']
#-- PORT CHECKS:
dont_nac_this = ["violation restrict","nterface Vlan",'ip address',"passive-interface","tacacs","mls netflow","source-interface","TenGigabitEthernet","mode trunk",'collect interface']
for ip in device_to_check:
	print (ip)
	ip = remove_return(ip)
	try:
        #-- CONNECTION CREDS:
		net_connect = netmiko.ConnectHandler(device_type='cisco_ios', ip=ip, username='your username', password='your password') 
		for command in commands:
			output = net_connect.send_command(command)
			for int_line in output.split("\n"):
                #--
                #-- NAC = FALSE:
				if "nterface" in int_line:
					if No_nac == True:
						print(interface)
					interface = int_line
					No_nac = True
                #--
                #-- NAC = TRUE:
				for each in dont_nac_this:
					if each in int_line:
						No_nac=False
	except:	
		print ("ERROR -FAILED TO FIND PORTS :-(")
#--
#-- *************************************************:
#-- END OF PYTHON SCRIPT                             :
#-- *************************************************: