#!/usr/bin/python
from scapy.all import *

victim = "192.168.203.129"
MAX_PACS = 40
packet = IP(dst=victim)

while MAX_PACS > 0: #sends MAX_PACS number of IP-layer-only packets
    reply = send(packet,verbose=False) 
    MAX_PACS-=1
    print('Packet sent to ['+victim+']')    
