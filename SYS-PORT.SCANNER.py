#--!/usr/bin/env python3
#-- -*- coding: Latin-1 -*-
#--
#-- **************************************************************************************************************:
#-- ********************************************* PORT VULNERABILITIES *******************************************:
#-- **************************************************************************************************************:
#-- Author:   JBALLARD (JEB)                                                                                      :
#-- Date:     2019.6.18                                                                                           :
#-- Script:   SYS-PORT.SCANNER.py                                                                                 :
#-- Purpose:  A python script that scans ports & identifies vulnerabilities.                                      :
#-- Version:  1.0                                                                                                 :
#-- **************************************************************************************************************:
#-- **************************************************************************************************************:
#--
#-- *************************************************:
#-- DEFINE PARAMS, CONFIG PATHS, IMPORT CLASSES      :
#-- *************************************************:
#-- python -m pip install IPy
#-- python -m pip install IP
#-- python -m pip install threading
#--
import socket 
from IPy import IP
import threading
#--
ports = []
banners = []
#--
def port_scanner(target,port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        try:
            trarget_ip =IP(target)
        except:
            target_ip = socket.gethostbyname(target)
        s.connect((target_ip, port))
        try:
            banner_name = banner(s).decode()
            ports.append(port)
            banners.append(banner_name.strip())
        except:
            pass
    except:
        pass
#--
#-- RETRIEVE BANNER NAME:
def banner(s):
    return s.recv(1024)
#--
#-- LOAD TARGET CONN DATA:
target = input("ENTER IP ADDRESS; LOCALHOST; OR DOMAIN NAME:")
#--
#-- SCAN 5051 FIRST:
for port in range(1,5051):
    thread = threading.Thread(target =port_scanner, args=[target,port])
    thread.start()
with open("vulnarable_banners.txt", "r") as file:
    data = file.read()
    for i in range(len(banners)):
        if banners[i] in data:
            print(f"[!]VULNERABILITY DISCOVERED: {banners[i]} @ PORT {ports[i]}")
#--
#-- DISPLAY INFO COMMAND LINE:
print ('COMPLETED SCAN IN: ', TOTAL)
#--
#-- **************************************************:
#-- END OF SCRIPT                                     :
#-- **************************************************:
