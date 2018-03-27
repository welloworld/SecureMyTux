#pragma once

//#include <linux/kernel.h>
//#include <linux/module.h>
//#include <linux/netfilter.h>
//#include <linux/skbuff.h>
/*#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/udp.h>
#include <linux/netfilter_ipv4.h>
#include <linux/netfilter_arp.h>
#include <asm-generic/errno.h>
#include <linux/in.h>
#include <asm/byteorder.h>
#include <linux/inet.h>
#include <linux/if_arp.h>
#include <net/arp.h>
#include <linux/etherdevice.h>
#include <linux/time.h>
#include <linux/delay.h>
*/
//#include <linux/moduleparam.h>

#include "Blacklist/blacklist.h"
#include "DOS_Detector/DOS_detector.h"
#include "ARP_Spoofing_Detector/arp_spoofing_detector.h"
#include "Rogue_DHCP_Detector/Rogue_DHCP_Detector.h"
#include "Rogue_DHCP_Detector/DHCP_Identification.h"

#include "log_protocol.h"

int __init main(void);
void __exit cleanup(void);
void _print_start_or_end(int exit);
void init_blacklist(void); 
void init_rogue_DHCP_detector(void);
void cleanup_blacklist(void);
void init_third_layer_filter(void);
unsigned int inbound_filter(void *priv, struct sk_buff *skb, const struct nf_hook_state *state);
asmlinkage int printdmesg(const char *fmt, ...);

static struct nf_hook_ops nfho_filter;

/*
Example:
blacklist_string_arg="aaaa,bbbb,cccccc", bl_len=3
*/
char* blacklist_string_arg; 
int bl_len=0;

module_param(blacklist_string_arg, charp,0);
module_param(bl_len,int,0);


/*
	'A' for arps, 'D' for DOS, 'R' for RogueDHCP, 'P' for patterns
	Examples: 	'ADRP' - everything
				'AP' - arps and patterns
				'DR' - DOS and RogueDHCP.......

*/
char* features_string_arg=NULL; 
int fe_len=0;

module_param(features_string_arg, charp,0);
module_param(fe_len,int,0);


char* dhcp_server_ip_arg=NULL;
int server_len=0;

module_param(dhcp_server_ip_arg, charp, 0);
module_param(server_len,int,0); //len(ip)
//For check quickly if component is on
int DOS_IS_ON = 0;
int ARP_IS_ON = 0;
int DHCP_IS_ON= 0;
int PATTERNS_IS_ON=0;
