#include "Rogue_DHCP_Detector.h"

/*
* This function is for initialization of the default DHCP server for the PC.
* The IP is constant while the component is on, and the PC wont get DHCP replies from another computers. 
* Input:
*	IP
*
* Output:
*	None		
*/
void init_dhcp_detector(char server[IP_ALEN],int len)
{
	long t;
	char temp_addr[IP_ALEN];
	unsigned short int curr_len=0;
	int addr_len=0;
	int i=0;
	for(i = 0; i < len; i++)
	{
		if(IP_SEPERATOR == server[i])
		{
			temp_addr[addr_len] = '\0';
			kstrtol(temp_addr, 10,&t);
			dhcp_server[curr_len++]=(unsigned char)t;
			addr_len=0;
		}
		else
		{
			temp_addr[addr_len] = server[i];
			addr_len++;
		}
		
	}
	temp_addr[addr_len] = '\0';
	//printk("%s\n",temp_addr);
	kstrtol(temp_addr, 10,&t);
	dhcp_server[curr_len++]=(unsigned char)t;	
	dmesg_dhcp("Default DHCP server: [%d.%d.%d.%d]\n",dhcp_server[0],dhcp_server[1],dhcp_server[2],dhcp_server[3]);
}

/*
* This function check whether the given IP is the default IP for DHCP.
* Input:
*	IP
* Output:
* 	TRUE if it is a rogue DHCP, otherwise FALSE.
*/
int is_rogue_dhcp(unsigned char ip[IP_ALEN])
{
	int i=0;
	for(i=0;i<IP_ALEN;i++)
	{
		if(ip[i] != dhcp_server[i])
		{
			dmesg_dhcp("Attack{RDHCP}: [%d.%d.%d.%d]\n",ip[0],ip[1],ip[2],ip[3]);
			return TRUE;
		}
	}
	return FALSE;
}
