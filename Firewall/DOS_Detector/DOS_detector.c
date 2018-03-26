#include "DOS_detector.h"

/*
* This function is for initialization of the DOS Detector.
*/
void init_DOS_detector(void)
{
	init_IP_pacs();
}

/*
* This function cleans the DOS Detector own blacklist.
*/
void clean_DOS_detector(void)
{
	struct IP_packets* temp;
	struct IP_packets* head = *IP_pacs;
	
	//Free IP packets:
	while((temp = head) != NULL)
	{
		head = head->_next_IP_packet;
		kfree(temp);
	}
}


/*
* This function checks if the source ip causes DOS.
* Input:
*	source ip
* Output:
*	TRUE if DOSed, otherwise FALSE
*/
int DOS_filter(unsigned char src_ip[])
{
	struct timespec timer;
	getnstimeofday(&timer);

	//The order of append, delete and dos is important!!!
	append_IP(src_ip,timer);
	delete_unrelevent_IPs();
	if(is_DOS(src_ip))
	{
		dmesg_dos("Attack{DOS}: [%d.%d.%d.%d]\n",src_ip[0],src_ip[1],src_ip[2],src_ip[3]);
		return TRUE;
	}

	return FALSE;
}


/* --------------------------------------- PRIVATE FUNCTIONS ---------------------------- */
/*
* This function is for initialization of the DOS Detector packets.
*/
void init_IP_pacs(void)
{
	IP_pacs = (struct IP_packets**) kmalloc(sizeof(struct IP_packets*), GFP_KERNEL);
	*IP_pacs = NULL;
}

/*
* This function is adding the source ip to the recently ips list.
* Input:
*	IP
*	timer when the packet has given
* Output:
*	None
*/
void append_IP(unsigned char src_ip[],struct timespec timer)
{
	//struct arphdr *arpHeader = arp_hdr(skb);
	struct IP_packets* new = (struct IP_packets*) kmalloc(sizeof(struct IP_packets), GFP_KERNEL);
	struct IP_packets* first = *IP_pacs;

	int i=0;
	new->_timer = timer;
	new->_next_IP_packet = NULL;

	for (i = 0; i < IP_LEN ; i++)
	{
		new->_src_ip[i] = src_ip[i];
	}

	if(*IP_pacs == NULL)
	{
		*IP_pacs = new;
	}
	else
	{
		while(first->_next_IP_packet != NULL)
		{ 
			first = first->_next_IP_packet;
		}
		first->_next_IP_packet = new;
	}

}

/*
* This function deletes unrelevent ips from the list, to keep recent ips relevent.
*/
void delete_unrelevent_IPs(void)
{
	struct timespec now;
	struct IP_packets* head = *IP_pacs;

	getnstimeofday(&now);
	while(head != NULL)
	{
		if(now.tv_sec - head->_timer.tv_sec > RELEVENT_SECONDS_FOR_DOS)
		{
			*(IP_pacs) = head->_next_IP_packet;
			//printk(KERN_INFO "GOING TO kfree - DANGEROUS!\n");// Kfree is friendly dont delete it its cute.
			kfree(head);
			head = *(IP_pacs);
		}
		else
		{
			break;
		}
	}
}

/*
* This function check whether the machine got DOSed or not.
* Input:
*	IP
* Output:
*	TRUE if DOSed, otherwise FALSE
*/
int is_DOS(unsigned char src_ip[IP_LEN])
{
	int counter=0;
	int flag=0;
	int i=0;
	struct IP_packets* temp = *IP_pacs;

	while(temp != NULL) // Count the amount of packets received from the same sender
	{
		flag=0;

		for(i=0;i<IP_LEN;i++)
		{
			if(src_ip[i] != temp->_src_ip[i])
			{
				flag = 1;
				break;
			}
		}

		if(!flag)
		{
			counter++;
		}
		temp = temp->_next_IP_packet;
	}
	//printk("%d\n",counter);
	if(counter >= NUMBER_OF_IPS_FOR_DOS)
	{
		return TRUE;
	}
	return FALSE;
}
