#include "arp_spoofing_detector.h"

/*
* This function is for initialization of the ARP Spoofing Detector.
*/
void init_arp_spoofing_detector(void)
{
	initArpPacs();
	initHooks();
}

/*
* This function cleans the ARP Spoofing Detector own blacklist.
*/
void clean_arp_spoofing_detector(void)
{
	struct arp_packets* temp;
	struct arp_packets* head = *arp_pacs;
	
	#if LINUX_VERSION_CODE >= KERNEL_VERSION(4,13,0)
		nf_unregister_net_hook(&init_net, &nfho_in_arp); //Need to be real vlue and not null
	#else
		nf_unregister_hook(&nfho_in_arp);
	#endif	
	//Free arp packets:
	while((temp = head) != NULL)
	{
		head = head->_next_arp_packet;
		kfree(temp);
	}
}

/*
* This function is for the initialization of the ARP packets list.
*/
void initArpPacs(void)
{
	arp_pacs = (struct arp_packets**) kmalloc(sizeof(struct arp_packets*), GFP_KERNEL);
	*arp_pacs = NULL;
}

/*
* This function is for the initialization of the ARP data to sniff.
*/
void initHooks(void)
{
	//FOR ARP:
	nfho_in_arp.hook		=  arp_filter;		// filter for inbound packets
	nfho_in_arp.hooknum 	= NF_ARP_IN;				// netfilter hook for local machine bounded ipv4 packets
	nfho_in_arp.pf			= NFPROTO_ARP;
	#if LINUX_VERSION_CODE >= KERNEL_VERSION(4,13,0)
		nf_register_net_hook(&init_net, &nfho_in_arp); //Need to be real vlue and not null
	#else
		nf_register_hook(&nfho_in_arp);
	#endif	
	//printk(KERN_INFO "ARP hook created successfully\n");
}

/*
* This function is for filtering the data and checks for ARP Spoofing.
* Input:
*	skb is the packet itselves
* Output:
*	NF_DROP if Spoofed, otherwise NF_ACCEPT
*/
unsigned int arp_filter(void *priv, struct sk_buff *skb, const struct nf_hook_state *state)
{
	struct ethhdr *hdr = eth_hdr(skb); 
	//printk(KERN_INFO "ARP Received\n");
	if(is_address_in_blacklist(NULL, hdr->h_source))
	{
		return NF_DROP;
	}
	else
	{
		struct timespec timer;

		getnstimeofday(&timer);

		//The order of append, delete and spoofing is important!!!
		append_packet(skb,timer);
		delete_unrelevent_packets();
		if(is_arp_spoofing(hdr->h_source))
		{

			dmesg_arp("Attack{ARPS}: [%pM]\n",hdr->h_source);
			append_to_blacklist(eth_hdr(skb)->h_source, ETH_ALEN);	
		}
	}

	return NF_ACCEPT;
}

/*
* This function appends the MAC to the blacklist of the ARP Spoofing Detector.
* Input:
*	skb is the packet itselves
*	timer
* Output:
*	None
*/
void append_packet(struct sk_buff *skb,struct timespec timer)
{
	struct arp_packets* new = (struct arp_packets*) kmalloc(sizeof(struct arp_packets), GFP_KERNEL);
	struct arp_packets* first = *arp_pacs;

	int i=0;
	new->_timer = timer;
	new->_next_arp_packet = NULL;

	for (i = 0; i < MAC_LEN ; i++)
	{
		new->_src_mac[i] = eth_hdr(skb)->h_source[i];
	}

	if(*arp_pacs == NULL)
	{
		*arp_pacs = new;
	}
	else
	{
		while(first->_next_arp_packet != NULL)
		{ 
			first = first->_next_arp_packet;
		}
		first->_next_arp_packet = new;
	}

}

/*
* This function deletes unrelevent macs from the list, to keep recent macs relevent.
*/
void delete_unrelevent_packets(void)
{
	struct timespec now;
	struct arp_packets* head = *arp_pacs;

	getnstimeofday(&now);
	while(head != NULL)
	{
		if(now.tv_sec - head->_timer.tv_sec > RELEVENT_SECONDS_FOR_SPOOF)
		{
			*(arp_pacs) = head->_next_arp_packet;
			//printk(KERN_INFO "GOING TO kfree - DANGEROUS!\n");// Kfree is friendly dont delete it its cute.
			kfree(head);
			head = *(arp_pacs);
		}
		else
		{
			break;
		}
	}
}

/*
* This function check whether the machine got ARP Spoofed or not.
* Input:
*	MAC
* Output:
*	TRUE if Spoofed, otherwise FALSE
*/
int is_arp_spoofing(unsigned char mac[MAC_LEN])
{
	int counter=0;
	int flag=0;
	int i=0;
	struct arp_packets* temp = *arp_pacs;

	while(temp != NULL) // Count the amount of arp received from the same sender
	{
		flag=0;

		for(i=0;i<MAC_LEN;i++)
		{
			if(mac[i] != temp->_src_mac[i])
			{
				flag = 1;
				break;
			}
		}

		if(!flag)
		{
			counter++;
		}
		temp = temp->_next_arp_packet;
	}
	if(counter >= NUMBER_OF_ARP_FOR_SPOOF)
	{
		return TRUE;
	}
	return FALSE;
}
