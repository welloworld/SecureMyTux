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
//#include <linux/netfilter_ipv4.h>
//#include <linux/netfilter_arp.h>
//#include <asm-generic/errno.h>
//#include <linux/in.h>
//#include <asm/byteorder.h>
//#include <linux/inet.h>
//#include <linux/if_arp.h>
#include <net/arp.h>
//#include <linux/etherdevice.h>
//#include <linux/time.h>
//#include <linux/delay.h>

#include "../log_protocol.h"

#define SEPERATOR ','// seperates addresses in blacklist string
#define IP_SEPERATOR '.'
#define MAC_SEPERATOR ':'
#define IP_ALEN 4// length in bytes
#define MAC_ALEN 6// length in bytes
#define TRUE 1
#define FALSE 0

typedef struct ip_node
{
	unsigned char ip[IP_ALEN];
	struct ip_node *_next;
} ip_node;


typedef struct mac_node
{
	unsigned char mac[MAC_ALEN];
	struct mac_node *_next;
} mac_node;


typedef struct blacklist
{
	// First place modification is still possible because the pointer is allocated inside a struct which points to it. GENIUS!
	struct mac_node* _mac_list;
	int mac_list_size;

	struct ip_node* _ip_list;
	int ip_list_size;
} blacklist;


void string_to_blacklist(char* str, int len);
char* blacklist_to_string( int* length);
void append_to_blacklist(unsigned char* addr, int addr_len);
void free_list(void);
int is_address_in_blacklist(unsigned char ip[],unsigned char mac[]);
void _init_blacklist(void);
void* alloc_node(int addr_len);

extern blacklist* bl;// Initialized in blacklist.c
