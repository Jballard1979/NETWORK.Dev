#!/usr/bin/env python3
#-- *************************************************************************************************************:
#-- ******************************************** OPEN NETWORK PORTS *********************************************:
#-- *************************************************************************************************************:
#-- Author:  JBallard (JEB)                                                                                      :
#-- Date:    2019.3.16                                                                                           :
#-- Script:  SYS-PORT.SCAN.v5.py                                                                                 :
#-- Purpose: A Python Script that pings a specified network port.                                                :
#-- Version: 1.0                                                                                                 :
#-- *************************************************************************************************************:
#-- *************************************************************************************************************:
#--
#-- *************************************************:
#-- DEFINE PARAMS, CONFIG PATHS, IMPORT CLASSES      :
#-- *************************************************:
import os
import sys
import socket
import datetime
import time
#--
FILE = os.path.join(os.getcwd(), "SCADA-PORT.SCAN.jeb")
#--
#-- PING SPECIFIED NETWORK IP & PORT:
def ping():
    try:
        socket.setdefaulttimeout(3)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #-
        #-- SET HOST IP ADDRESS & PORT:
        host = "10.165.10.17"
        port = 3389
        #-
        server_address = (host, port)
        s.connect(server_address)
    except OSError as error:
        return False
    else:
        s.close()
        return True
#--
#-- CONNECTION TIME (SEC):
def calculate_time(start, stop):
    difference = stop - start
    seconds = float(str(difference.total_seconds()))
    return str(datetime.timedelta(seconds=seconds)).split(".")[0]
#-
#-- CONNECTION STATUS:
def first_check():
    if ping():
        #-- IF PING SUCCESSFULL:
        live = "\nCONNECTION ACQUIRED\n"
        print(live)
        connection_acquired_time = datetime.datetime.now()
        acquiring_message = "CONNECTION ACQUIRED @: " + \
            str(connection_acquired_time).split(".")[0]
        print(acquiring_message)
        with open(FILE, "a") as file:
            #-- WRITE TO LOG:
            file.write(live)
            file.write(acquiring_message)
        return True
    else:
        #-- IF PING FAILED:
        not_live = "\nCONNECTION NOT ACQUIRED\n"
        print(not_live)
 
        with open(FILE, "a") as file:
            #-- WRITE TO LOG:
            file.write(not_live)
        return False
#--
#-- MAIN FUNCTION:
def main():
    monitor_start_time = datetime.datetime.now()
    monitoring_date_time = "MONITORING BEGAN @: " + \
        str(monitor_start_time).split(".")[0]
    #--
    if first_check():
        print(monitoring_date_time)
    else:
        while True:
            if not ping():
                time.sleep(1)
            else:
                first_check()
                print(monitoring_date_time)
                break
    with open(FILE, "a") as file:
        file.write("\n")
        file.write(monitoring_date_time + "\n")
    while True:
        if ping():
            time.sleep(5)
        else:
            down_time = datetime.datetime.now()
            fail_msg = "DISCONNECTED @: " + str(down_time).split(".")[0]
            print(fail_msg)
            with open(FILE, "a") as file:
                file.write(fail_msg + "\n")
            #--
            while not ping():
                time.sleep(1)
            up_time = datetime.datetime.now()
            uptime_message = "CONNECTION ESTABLISHED: " + str(up_time).split(".")[0]
            down_time = calculate_time(down_time, up_time)
            unavailablity_time = "CONNECTION AVAILABLE FOR: " + down_time
            #--
            print(uptime_message)
            print(unavailablity_time)
            with open(FILE, "a") as file:
                file.write(uptime_message + "\n")
                file.write(unavailablity_time + "\n")
main()
#--
#-- *************************************************:
#-- END OF PYTHON SCRIPT                             :
#-- *************************************************:
