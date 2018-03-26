#pragma once

#include <linux/kernel.h>
#include <linux/module.h>
//#include <linux/netfilter.h>
//#include <linux/netfilter_ipv4.h>
//#include <linux/skbuff.h>
//#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/udp.h>

#include "../log_protocol.h"

#define DHCP_SERVER_PORT 67
#define DHCP_CLIENT_PORT 68
#define TRUE 1
#define FALSE 0

int is_udp(struct sk_buff *skb);
int is_dhcp(struct sk_buff *skb);
void dhcp_pkt_type(struct sk_buff *skb);
