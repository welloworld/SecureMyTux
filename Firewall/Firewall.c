#include "Firewall.h"

/*
* This function is the main function of the component. It inits some standalone code as the Netfiler Hook for third layer, and the blacklist for block addresses.
* Moreover, The whole component is given an argument of which components are going to work.
* Input of component: 
*	blacklist_string_arg is the argument of the blacklist, gets ips and macs as 4 or 6 bytes represented. 
*	bl_len is the number of the ips and macs to block, how many ips and macs we got as argument.
*	features_string_arg is which components are going to work, 'A' for arps, 'D' for DOS, 'R' for RogueDHCP.
*	fe_len is the number of features we ot as argument.
*	dhcp_server_ip_arg is the default dhcp server to get dhcp replies only from him.
* Output:
*	None
*/
int __init main(void)
{
	int i=0;
	init_blacklist();
	init_third_layer_filter();
	//printk("Over here!\n");
	//_print_start_or_end(0); //0 means we just started the module

	for(i=0;i<fe_len;i++)
	{
		switch (features_string_arg[i])
		{
			case 'R': //Rogue DHCP
				DHCP_IS_ON=1;
				dmesg_dhcp("On:\n");
				init_rogue_DHCP_detector();
				break;

			case 'A': //ARP SPOOFING
				ARP_IS_ON=1;
				dmesg_arp("On:\n");
				init_arp_spoofing_detector();
				break;
			case 'D': //DOS
				DOS_IS_ON=1;
				dmesg_dos("On:\n");
				init_DOS_detector();
				break;
			
			case 'P': //PATTERNS
				PATTERNS_IS_ON=1;
				//dmesg("On:\n");    //If component will add, please add a dmesg function!
				//init_patterns_detector();
				break;

			default:
				dmesg_error("Incorrect features argument!\n");
				break;
		}
	}

	return 0;
}


void __exit cleanup(void)
{
	#if LINUX_VERSION_CODE >= KERNEL_VERSION(4,13,0)
		nf_unregister_net_hook(&init_net, &nfho_filter); //Need to be real vlue and not null
	#else
		nf_unregister_hook(&nfho_filter);
	#endif	
	
	if(ARP_IS_ON)
	{
		clean_arp_spoofing_detector();
	}
	if(DOS_IS_ON)
	{
		clean_DOS_detector();
	}
   	if(PATTERNS_IS_ON)
   	{
   		//clean_patterns_detector();
   	}

   	cleanup_blacklist();
   	//_print_start_or_end(1); //1 means we are going to exit
	//dmesg_firewall("Cleaned my MESS\n   Stay Calm\n     And \n   Keep Linux\n");
}

/*void _print_start_or_end(int exit)
{
	unsigned long get_time;
	int tmp1,tmp2;
	struct timeval tv;
	int curr_time[3]; //[0] is sec,[1] is min,[2] is hour

	do_gettimeofday(&tv);

	get_time = tv.tv_sec;
	curr_time[0] = get_time % 60;
	tmp1 = get_time / 60;
	curr_time[1] = tmp1 % 60;
	tmp2 = tmp1 / 60;
	curr_time[2] = tmp2 % 24;
	
	//Change to Israel time (+2:00)
	curr_time[2] += 2;
	if(exit)
	{
		//dmesg("ENDED %02d:%02d:%02d\n",curr_time[2],curr_time[1],curr_time[0]);
		dmesg_firewall("ENDED\n");
	}
	else
	{
		//dmesg("STARTED %02d:%02d:%02d\n",curr_time[2],curr_time[1],curr_time[0]);
		dmesg_firewall("STARTED\n");
	}
	
}*/

/*
* The blacklist is an extern variable named bl. It's origin is blacklist.h . 
* It's being used to keep a blacklist of addresses which we shall not accept traffic from.
*/
void init_blacklist(void)
{
	string_to_blacklist(blacklist_string_arg,bl_len);	
}

/*
* This function is for initialization of the default DHCP server for the PC.
* The IP is constant while the component is on, and the PC wont get DHCP replies from another computers. 
*/
void init_rogue_DHCP_detector(void)
{
	init_dhcp_detector(dhcp_server_ip_arg,server_len);
}

/*
* This function is for cleanup the blacklist of the addresses to block.
*/
void cleanup_blacklist(void)
{
	//If we come to change the blacklist in the firewall we somehow need to save it in the blacklist FILE!!.
	// We can run the GUI with parameter and the GUI will update it. or find another way...

	// Free blacklist
	free_list();

}

/*
* This function is for initialization of sniffing data from the third layer and up.
* It uses Netfilter hooks to 'hook' our code into the network component of the computer, which gives us the ability to drop packets. 
*/
void init_third_layer_filter(void)
{
	nfho_filter.hook		= inbound_filter;		// filter for inbound packets
	nfho_filter.hooknum 	= NF_INET_PRE_ROUTING;				// netfilter hook for local machine bounded ipv4 packets
	nfho_filter.pf			= PF_INET;//ETH_P_ALL;	
	nfho_filter.priority 	= NF_IP_PRI_FIRST;			
	#if LINUX_VERSION_CODE >= KERNEL_VERSION(4,13,0)
		nf_register_net_hook(&init_net, &nfho_filter); //Need to be real vlue and not null
	#else
		nf_register_hook(&nfho_filter);
	#endif	
	
	//dmesg_firewall("Firewall filter hook created successfully\n");
}

/*
* This function is the main filter of the Firewall component
* It gets the IP and the Mac from each packet we get, and check if the ip/mac is in the blacklist of addresses to block,
* if so we're dropping the packet, otherwise we check by the user wanted components, if to check DOS and Rogue DHCP.
* NOTE: ARP Spoofing is a standalone component, if it detects a Spoofing, it will automaticlly add the mac to the blacklist.
* Input:
*	skb is the packet structure, for every layer we need to get the layer by using netfilter function and pointers.
*	Other inputs are not interesting
* 
* Output:
*	NF_DROP to drop the packet, and NF_ACCEPT for accept the packet.			
*/
unsigned int inbound_filter(void *priv, struct sk_buff *skb, const struct nf_hook_state *state)
{
	int i=0;
	unsigned char* ip = NULL;
	unsigned char mac[MAC_ALEN];

	struct ethhdr *ethHeader = eth_hdr(skb);
	struct iphdr *ipHeader = ip_hdr(skb);; 
	
	// Extract packet ip and mac
	for(i=0;i<MAC_ALEN;i++)
	{
		mac[i]=ethHeader->h_source[i];
	}

	if(ethHeader->h_proto == ntohs(ETH_P_IP))
	{
		ip = (unsigned char*)&ipHeader->saddr;
		//dmesg("Packet from [%02x:%02x:%02x:%02x:%02x:%02x][%d.%d.%d.%d]\n",mac[0],mac[1],mac[2],mac[3],mac[4],mac[5],ip[0],ip[1],ip[2],ip[3]);
	}
	
	// FILTER
	if(is_address_in_blacklist(ip,mac)) //Function checks whether the ip is null or not
	{
		if(ip)
		{
			dmesg_firewall("Droped: [%02x:%02x:%02x:%02x:%02x:%02x][%d.%d.%d.%d]\n",mac[0],mac[1],mac[2],mac[3],mac[4],mac[5],ip[0],ip[1],ip[2],ip[3]);
		}
		else
		{
			dmesg_firewall("Droped: [%02x:%02x:%02x:%02x:%02x:%02x]\n",mac[0],mac[1],mac[2],mac[3],mac[4],mac[5]);
		}
		return NF_DROP;
	}
	else
	{
		if(DOS_IS_ON)
		{
			if(ip != NULL && DOS_filter(ip))
			{
				append_to_blacklist(ip, IP_LEN);
			}
		}
		if(DHCP_IS_ON)
		{
			if(ip != NULL && is_dhcp(skb))
			{
				if(is_rogue_dhcp(ip))
				{
					append_to_blacklist(ip, IP_LEN);
				}
			}
		}
	}

	//dmesg("Packet captured\n");	
	return NF_ACCEPT;
}


module_init(main);
module_exit(cleanup);

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Here to secure you");
MODULE_AUTHOR("Yan Poran & Nevo Biton");
