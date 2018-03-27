#!/usr/bin/python
from scapy.all import *

server_ip="192.168.43.90"        #My IP
client_ip="192.168.43.40" 	     #Made up IP
server_mac="C4:8E:8F:C1:BD:05"   #My MAC
client_mac="04:0c:ce:e0:ef:64"   #Client's MAC
subnet_mask="255.255.255.0"      #Made up subnet
gateway="192.168.43.1"           #Made up gateway

pkt = Ether(src=server_mac,dst="ff:ff:ff:ff:ff:ff")
pkt /= IP(src=server_ip,dst="255.255.255.255")
pkt /= UDP(sport=67,dport=68)
pkt /= BOOTP(op=2,yiaddr=client_ip,siaddr=server_ip,giaddr=gateway,chaddr=client_mac)
pkt /= DHCP(options=[("message-type", "offer")])
pkt /= DHCP(options=[('subnet_mask',subnet_mask)])
pkt /= DHCP(options=[('server_id',server_ip),('end')])

sendp(pkt)