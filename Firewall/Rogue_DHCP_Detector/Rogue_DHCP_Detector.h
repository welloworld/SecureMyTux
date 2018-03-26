#pragma once

#include <linux/kernel.h>
#include <linux/module.h>
//#include <linux/ip.h>
//#include <linux/if_ether.h>
//#include <linux/inet.h>
//#include <linux/netfilter.h>
//#include <linux/skbuff.h>
//#include <linux/ip.h>
//#include <linux/tcp.h>
//#include <linux/udp.h>
#include <linux/netfilter_ipv4.h>
//#include <linux/netfilter_arp.h>
//#include <asm-generic/errno.h>
//#include <linux/in.h>
//#include <asm/byteorder.h>
//#include <linux/inet.h>
//#include <linux/if_arp.h>
//#include <net/arp.h>
//#include <linux/etherdevice.h>
//#include <linux/time.h>
//#include <linux/delay.h>

#include "../log_protocol.h"

#define IP_ALEN 4
#define TRUE 1
#define FALSE 0
#define IP_SEPERATOR '.'

void init_dhcp_detector(char ip[IP_ALEN],int len);
int is_rogue_dhcp(unsigned char ip[IP_ALEN]);

static unsigned char dhcp_server[IP_ALEN];
