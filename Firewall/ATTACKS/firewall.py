#!/usr/bin/python
from scapy.all import *

victim = "192.168.203.129"
TIMEOUT=2
MAX_PING = 20
packet = IP(dst=victim)/ICMP()

while MAX_PING > 0: #Trying send pings.
    reply = sr1(packet, timeout=TIMEOUT,verbose=False)
    if not (reply is None):
         print reply.dst, " got pinged"
    else:
         print "Timeout waiting for %s" % packet[IP].dst
    MAX_PING-=1     
