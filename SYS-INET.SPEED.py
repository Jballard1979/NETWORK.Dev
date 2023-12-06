#--
#-- ************************************************************************************************************:
#-- ****************************************** CHECK INTERNET SPEEDS *******************************************:
#-- ************************************************************************************************************:
#-- Author:   JBALLARD (JEB)                                                                                    :
#-- Date:     2023.3.07                                                                                         :
#-- Script:   SYS-INET.SPEED.py                                                                                 :
#-- Purpose:  A python script that checks your internet speed using the Speedtest-CLI module.                   :
#-- Version:  1.0                                                                                               :
#-- ************************************************************************************************************:
#-- ************************************************************************************************************:
#--
#-- *************************************************:
#-- DEFINE PARAMS, CONFIG PATHS, IMPORT CLASSES      :
#-- *************************************************:
PYTON -m PIP INSTALL pyspeedtest
PYTON -m PIP INSTALL speedtest
PYTON -m PIP INSTALL speedtest-cli
#--
import speedtest
import pyspeedtest
#--
def test_internet_speed():
    #-- USE SPEEDTEST MODULE:
    speed_test = speedtest.Speedtest()
    best_server = speed_test.get_best_server()
    print(f"Best server: {best_server['host']} located in {best_server['country']}")
    download_speed = speed_test.download() / 1_000_000  # Convert to Mbps
    print(f"Download speed: {download_speed:.2f} Mbps")
    upload_speed = speed_test.upload() / 1_000_000  # Convert to Mbps
    print(f"Upload speed: {upload_speed:.2f} Mbps")
    #-- USE PYSPEEDTEST MODULE:
    pst = pyspeedtest.SpeedTest()
    ping_speed = pst.ping()
    print(f"Ping speed: {ping_speed} ms")
#--
if __name__ == "__main__":
    test_internet_speed()
#--
#-- *************************************************:
#-- END OF SCRIPT                                    :
#-- *************************************************: