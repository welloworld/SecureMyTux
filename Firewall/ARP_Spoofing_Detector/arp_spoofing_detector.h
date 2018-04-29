/* Kernel module for securing your extra supportive and awesome linux os. 
 * Made by Yan Poran & Nevo Biton, thanks to our mind-blowing guide, made
 * of greatness: Liad Eliahu
 * And with that, a round of applause for your new bodyguard: TTM!
 * Trust The Module ;)
*/
#pragma once
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/version.h>
//#include <linux/netfilter.h>
//#include <linux/skbuff.h>
//#include <linux/ip.h>
//#include <linux/tcp.h>
//#include <linux/udp.h>
//#include <linux/netfilter_ipv4.h>
#include <linux/netfilter_arp.h>
//#include <asm-generic/errno.h>
//#include <linux/in.h>
//#include <asm/byteorder.h>
//#include <linux/inet.h>
//#include <linux/if_arp.h>
//#include <net/arp.h>
//#include <linux/etherdevice.h>
//#include <linux/time.h>
//#include <linux/delay.h>

#include "../Blacklist/blacklist.h"
#include "../log_protocol.h"

#define NUMBER_OF_ARP_FOR_SPOOF 5
#define RELEVENT_SECONDS_FOR_SPOOF 5
#define MAC_LEN 6
#define TRUE 1
#define FALSE 0

void init_arp_spoofing_detector(void);
void clean_arp_spoofing_detector(void);
void initArpPacs(void);
void initHooks(void);
unsigned int arp_filter(void *priv, struct sk_buff *skb, const struct nf_hook_state *state);
void append_packet(struct sk_buff *skb,struct timespec timer);
void delete_unrelevent_packets(void);
int is_arp_spoofing(unsigned char mac[MAC_LEN]);


typedef struct arp_packets
{
	unsigned char _src_mac[MAC_LEN];
	struct timespec _timer;
	struct arp_packets* _next_arp_packet;
} arp_packets;

static struct nf_hook_ops nfho_in_arp;

static struct arp_packets** arp_pacs = NULL;// initialized in main;
