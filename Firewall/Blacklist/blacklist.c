#include "blacklist.h"

blacklist *bl = NULL;// MUST be initialized here because it is defined in blacklist.h. DON'T change. for info: https://stackoverflow.com/questions/1433204/how-do-i-use-extern-to-share-variables-between-source-files

/*
* This function takes a formated string and converts it into a blacklist.
* Input: 
*	string in the following format: 127.0.0.1.,192.168.1.1.,...
* and a , between each address. Can contain many addresses and the order doesn't have an effect 
*	len is the length of the string
* Output:
*	blacklist
*/
void string_to_blacklist(char str[], int len)
{
	
	int i;
	long t;
	char temp_addr[ETH_ALEN];// using mac addr length because it has enough space for mac addr or ip addr
	unsigned short int addr_len;
	unsigned char curr_addr[ETH_ALEN];
	int curr_len=0;
	int j=0;
	//unsigned char t = str[0];
	_init_blacklist();
	
	//printk("In string_to_blacklist\n");
	//printk("string to black: %s %lu %s\n",str,long_address,dot_ip);
	addr_len = 0;
	for(i = 0; i < len; i++)
	{
		if(IP_SEPERATOR == str[i])
		{
			temp_addr[addr_len] = '\0';
			//printk("%s\n",temp_addr);
			kstrtol(temp_addr, 10,&t);
			curr_addr[curr_len++]=(unsigned char)t;	

			addr_len = 0;
		}
		else if(MAC_SEPERATOR == str[i])
		{
			temp_addr[addr_len] = '\0';
			//printk("%s\n",temp_addr);
			kstrtol(temp_addr, 16,&t);
			curr_addr[curr_len++]=(unsigned char)t;	

			addr_len = 0;
		}
		else if(SEPERATOR == str[i])
		{
			
			//printk("%d\n",curr_len);
			if(IP_ALEN == curr_len)
			{
				//dmesg_blacklist("Trying IP to the blacklist $@#: [%d.%d.%d.%d]\n",curr_addr[0],curr_addr[1],curr_addr[2],curr_addr[3]);
				// add the address to the ip_list
				append_to_blacklist(curr_addr, IP_ALEN);
				for(j=0;j<IP_ALEN;j++)
				{
					curr_addr[j] = '\0';
				}
			}
			else
			{
				//dmesg_blacklist("Trying MAC to the blacklist: [%02x:%02x:%02x:%02x:%02x:%02x]\n",curr_addr[0],curr_addr[1],curr_addr[2],curr_addr[3],curr_addr[4],curr_addr[5]);
				// add the address to the mac_list
				append_to_blacklist(curr_addr, MAC_ALEN);
				for(j=0;j<MAC_ALEN;j++)
				{
					curr_addr[j] = '\0';
				}
			}
			
			//reset addr count
			//printk("addr_len: %d\n", addr_len);
			curr_len = 0;
		}
		else
		{
			temp_addr[addr_len] = str[i];
			//printk("appendg %c %c %d\n",temp_addr[addr_len],str[i],addr_len);
			addr_len++;
		}
		
	}
	//dmesg_blacklist("Appending IP to the blacklist: [%s]\n",str);
	

}


/* 
* This function converts the current blacklist into string.
* Input: 
*	Pointer to length of the string
* Output:
*	the blacklist Itselves
*/
char* blacklist_to_string(int * length)
{
	int len = ((bl->mac_list_size * (MAC_ALEN + 1)) + (bl->ip_list_size * (IP_ALEN + 1)));
	ip_node* ip_head = bl->_ip_list;
	mac_node* mac_head = bl->_mac_list;
	
	char * res = (char *)kmalloc(len * sizeof(char), GFP_KERNEL);
	int res_i = 0;
	int i = 0;
	
	while(NULL != ip_head)
	{
		for(i = 0; i < IP_ALEN; i++, res_i++) { res[res_i] = ip_head->ip[i]; }
		res[res_i] = SEPERATOR;
		res_i++;
		ip_head = ip_head->_next;
	}
	
	while(NULL != mac_head)
	{
		for(i = 0; i < MAC_ALEN; i++, res_i++) { res[res_i] = mac_head->mac[i]; }
		res[res_i] = SEPERATOR;
		res_i++;
		mac_head = mac_head->_next;
	}

	res[res_i] = 0;	
	*length = len;
	return res;
}

/*
* This function appends the address to the blacklist
* Input:
*	address (IP or MAC)
* Output:
*	None
*/
void append_to_blacklist(unsigned char *addr, int addr_len)
{
	int i = 0;// used for deep copy address
	mac_node* last_mac;
	if(IP_ALEN == addr_len)// its an ip node
	{
		ip_node * last = bl->_ip_list;
		if(NULL == last)
		{
			bl->_ip_list = (ip_node*)alloc_node(IP_ALEN);
			last = bl->_ip_list;
			for(i = 0; i < IP_ALEN; i++) { last->ip[i] = addr[i]; }
			last->_next = NULL;
		}
		else
		{
			while(NULL != last->_next)
			{
				last = last->_next;
			}

			last->_next = (ip_node*)alloc_node(IP_ALEN);
			for(i = 0; i < IP_ALEN; i++) { last->_next->ip[i] = addr[i]; }
			last->_next->_next = NULL;
		}

		bl->ip_list_size++;
		dmesg_blacklist("Appending IP to the blacklist: [%d.%d.%d.%d]\n",addr[0],addr[1],addr[2],addr[3]);
		

	}
	else// its a mac node
	{
		last_mac = bl->_mac_list;

		if(NULL == last_mac)
		{
			bl->_mac_list = (mac_node*)alloc_node(MAC_ALEN);
			last_mac = bl->_mac_list;
			for(i = 0; i < MAC_ALEN; i++) { last_mac->mac[i] = addr[i]; }
			last_mac->_next = NULL;
		}
		else
		{
			while(NULL != last_mac->_next)
			{
				last_mac = last_mac->_next;
			}

			last_mac->_next = (mac_node*)alloc_node(MAC_ALEN);
			for(i = 0; i < MAC_ALEN; i++) { last_mac->_next->mac[i] = addr[i]; }
			last_mac->_next->_next = NULL;
		}

		bl->mac_list_size++;
		dmesg_blacklist("Appending MAC to the blacklist: [%02x:%02x:%02x:%02x:%02x:%02x]\n",addr[0],addr[1],addr[2],addr[3],addr[4],addr[5]);
	}
}

/*
* This function is for the cleanup of the Blacklist list.
*/
void free_list(void)
{
	mac_node *headMAC;
	mac_node *currMAC;

	ip_node *headIP;
	ip_node *currIP;
	
	headIP = bl->_ip_list;
	if(0 < bl->ip_list_size)
	{
		while ((currIP = headIP) != NULL) // set curr to head, stop if list empty.
		{ 
			headIP = headIP->_next;          // advance head to next element.
			kfree(currIP);                // delete saved pointer.
		}
	}

	headMAC = bl->_mac_list;
	if(0 < bl->mac_list_size)
	{
		while ((currMAC = headMAC) != NULL) // set curr to head, stop if list empty.
		{ 
			headMAC = headMAC->_next;          // advance head to next element.
			kfree(currMAC);                // delete saved pointer.
		}
	}

	kfree(bl);
}

/*
* This function checks whether the ip or the mac is in the list already.
* Input:
*	IP
* 	MAC
* Output:
*	TRUE if it is in the blacklist, otherwise false
*/
int is_address_in_blacklist(unsigned char ip[],unsigned char mac[])
{
	int i=0;
	int j=0;
	int flag=0;
	struct mac_node* temp_mac = bl->_mac_list;
	struct ip_node* temp_ip = NULL;
	if(ip)
	{
		temp_ip = bl->_ip_list;
		for(i=0; i< bl->ip_list_size;i++)
		{
			//printk("[%d.%d.%d.%d] - [%d.%d.%d.%d]\n",temp_ip->ip[0],temp_ip->ip[1],temp_ip->ip[2],temp_ip->ip[3],ip[0],ip[1],ip[2],ip[3]);
			flag=0;
			for(j=0; j < IP_ALEN ; j++)
			{
				if(temp_ip->ip[j] != ip[j])
				{
					flag=1;
				}
			}
			if(!flag)
			{
				return TRUE;
			}
			temp_ip = temp_ip->_next;
		}
	}
	for(i=0; i< bl->mac_list_size;i++)
	{
		flag=0;
		for(j=0; j < MAC_ALEN ; j++)
		{
			if(temp_mac->mac[j] != mac[j])
			{
				flag=1;
			}
		}
		if(!flag)
		{
			return TRUE;
		}
		temp_mac = temp_mac->_next;
	}
	return FALSE;
}


/*-------------------------------PRIVATE FUNCTIONS---------------------------------*/

/*
* This function is for initialization of the Blacklist.
*/
void _init_blacklist(void)
{
	bl = (struct blacklist*) kmalloc(sizeof(blacklist), GFP_KERNEL);
	bl->_mac_list = NULL;
	bl->_ip_list = NULL;
	bl->mac_list_size = 0;
	bl->ip_list_size = 0;
}

/*
* This function is for allocating a node in the blacklist list.
* Input:
* 	address length
* Output:
*	pointer to allocated memory
*/
void * alloc_node(int addr_len)
{
	if(IP_ALEN == addr_len)
	{
		return (ip_node *)kmalloc(sizeof(ip_node), GFP_KERNEL);
	}
	else
	{
		return (mac_node *)kmalloc(sizeof(mac_node), GFP_KERNEL);
	}
}
