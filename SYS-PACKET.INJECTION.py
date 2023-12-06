#-- *************************************************************************************************************:
#-- ********************************************* PACKET INJECTION **********************************************:
#-- *************************************************************************************************************:
#-- Author:  JBallard (JEB)                                                                                      :
#-- Date:    2017.11.06                                                                                          :
#-- Script:  SYS-PACKET.INJECTION.py                                                                             :
#-- Purpose: A Python Script that injects packets into a TCP/IP Layer stream.                                    :
#-- Usage:   IEX(New-Object Net.WebClient).downloadString('https://platform.activestate.com/dl/cli/install.ps1') :
#-- Version: 1.0                                                                                                 :
#-- *************************************************************************************************************:
#-- *************************************************************************************************************:
#--
#-- *************************************************:
#-- DEFINE PARAMS, CONFIG PATHS, IMPORT CLASSES      :
#-- *************************************************:
import socket
import struct
from random import randint
#--
#-- BUILD ICMP PACKET:
def create_icmp_packet():
   type = 8
   code = 0
   chksum = 0
   id = randint(0, 0xFFFF)
   seq = 1
   checksum = calculate_checksum(struct.pack("!BBHHH", type, code, chksum, id, seq))
   packet = struct.pack("!BBHHH", type, code, socket.htons(checksum), id, seq)
   return packet
#--
#-- CALC CHECKSUM FOR PACKET:
def calculate_checksum(packet):
   s = 0
   n = len(packet) % 2
   for i in range(0, len(packet) - n, 2):
       s += packet[i] + (packet[i + 1] << 8)
   if n:
       s += packet[i + 1]
   while s >> 16:
       s = (s & 0xFFFF) + (s >> 16)
   s = ~s & 0xFFFF
   return s
#--
#-- WRITE ICMP PACKET:
def main():
   s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
   s.sendto(create_icmp_packet(), ("10.165.3.42", 80))
#--
if __name__ == "__main__":
  main()
#--
#-- *************************************************:
#-- END OF PYTHON SCRIPT                             :
#-- *************************************************:
