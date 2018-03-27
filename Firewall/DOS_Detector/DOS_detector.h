#pragma once
#include <linux/kernel.h>
#include <linux/module.h>
//#include <linux/netfilter.h>
//#include <linux/skbuff.h>
#include <linux/ip.h>
//#include <linux/tcp.h>
//#include <linux/udp.h>
//#include <linux/netfilter_ipv4.h>
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

#define NUMBER_OF_IPS_FOR_DOS 30
#define RELEVENT_SECONDS_FOR_DOS 4
#define IP_LEN 4
#define TRUE 1
#define FALSE 0

void init_DOS_detector(void);
void clean_DOS_detector(void);
void init_IP_pacs(void);
int DOS_filter(unsigned char src_ip[]);
void append_IP(unsigned char src_ip[],struct timespec timer);
void delete_unrelevent_IPs(void);
int is_DOS(unsigned char ip[IP_LEN]);


typedef struct IP_packets
{
	unsigned char _src_ip[IP_LEN];
	struct timespec _timer;
	struct IP_packets* _next_IP_packet;
} IP_packets;


static struct IP_packets** IP_pacs = NULL;// initialized in init_DOS_detector;
