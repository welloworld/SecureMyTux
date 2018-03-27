#include "DHCP_Identification.h"

int is_udp(struct sk_buff *skb)
{
	//The firewall call this function only if the packet has IP layer
	struct iphdr *ip_header;
	
	ip_header = ip_hdr(skb);
	if (ip_header->protocol == IPPROTO_UDP)
		return 1;
	return 0;
}

/*
* This function checks whether the packet is dhcp or not.
* Input:
*	skb
* Output:
*	TRUE is it is DHCP, otherwise FALSE. 
*/
int is_dhcp(struct sk_buff *skb)
{
	struct udphdr *udp_header;
	if (is_udp(skb))
	{
		udp_header = (struct udphdr *)udp_hdr(skb);
		if (udp_header->source == htons(DHCP_SERVER_PORT) || udp_header->dest == htons(DHCP_SERVER_PORT) ||	(udp_header->source == htons(DHCP_CLIENT_PORT)) || (udp_header->dest == htons(DHCP_CLIENT_PORT))) 
		{
			return TRUE;
		}
	}
	return FALSE;
}

/*
* Print the value of 'type', and block only 'offer' request
* Do we need that function ?
*/
void dhcp_pkt_type(struct sk_buff *skb)
{

	struct udphdr *udp_header;
	unsigned char *udp_data;
	unsigned int type = 0, type_offset = 0;
	/*u_int8_t op, htype;*/

	udp_header = udp_hdr(skb);
	/* get start of udp data*/
	udp_data = ((char *)udp_header + sizeof(struct udphdr));
	/*type = *((int*)(udp_data + sizeof(struct udphdr)));*/
	type_offset = 1+1+1+1+4+2+2+4+4+4+4+16+64+128+4+2;
	type = *(udp_data + type_offset);  /* type is 1 byte data */
	//printk(KERN_DEBUG"%s%s %s: dhcp-packet type %d\n", MODULE_SIGNATURE, RDHCP_PREFIX, __func__, type);

	return ;
}