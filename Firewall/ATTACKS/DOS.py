#!/usr/bin/python
from scapy.all import *
victim = "192.168.203.129"
MAX_PACS = 20
packet = IP(dst=victim)
while MAX_PACS > 0:
    reply = send(packet,verbose=False)
    MAX_PACS-=1
    print 'Packet sent to ['+victim+']'    
