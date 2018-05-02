import subprocess
import os
from time import sleep
"""
This component is the Logger! :-}
It reads from the dmesg (the kernel modules output)
And write it to divided logs
IMPORTANT: The program must runs with sudo ---> sudo python2 Logger.py
Have fun and keep Linux 

SecureMyTux Team ;->
"""

LOGS_DIR = '/var/log/smt' 

#Our module communication protocol
MODULE_SIGNATURE = '[SMT]'

FIREWALL_MISC = '[FM]'
FIREWALL_ARP = '[FA]'
FIREWALL_DOS = '[FD]'
FIREWALL_RDHCP = '[FR]'
FIREWALL_BLACKLIST = '[FB]'

SYSCALL_HOOKING_MANAGER = '[SH]'
SYSCALL_HOOKING_FILES = '[SF]'
SYSCALL_HOOKING_SOCKETS = '[SS]'
SYSCALL_HOOKING_DIRS = '[SD]'
SYSCALL_HOOKING_PERMISSIONS = '[SP]'
SYSCALL_HOOKING_FDS = '[SC]'
SYSCALL_HOOKING_EXECUTIONS = '[SE]'


ARP_KEY = 'FW_ARP'
DOS_KEY = 'FW_DOS'
RDHCP_KEY = 'FW_DHCP'
MISC_KEY = 'FW_MISC'
BLACKLIST_KEY = 'FW_BL'
SHM_MANAGER_KEY = 'SHM_SH'
SHM_FILES_KEY = 'SHM_SF'
SHM_SOCKETS_KEY = 'SHM_SS'
SHM_DIRS_KEY = 'SHM_SD'
SHM_PERMISSIONS_KEY = 'SHM_SP'
SHM_FDS_KEY = 'SHM_SC'
SHM_EXECUTIONS_KEY = 'SHM_SE'


NUMBER_OF_SECS_TO_SLEEP=10 #Reads the logs every <NUMBER_OF_SECS_TO_SLEEP> secs
tail=1 #1 is ok
#variables

logs_by_affiliation = {
	ARP_KEY: [],
	DOS_KEY: [],
	RDHCP_KEY: [],
	MISC_KEY: [],
	SHM_MANAGER_KEY: [],
	SHM_FILES_KEY: [],
	SHM_SOCKETS_KEY: [],
	SHM_DIRS_KEY: [],
	SHM_PERMISSIONS_KEY: [],
	SHM_FDS_KEY: [],
	SHM_EXECUTIONS_KEY: [],
        BLACKLIST_KEY: []
}


#get dmesg output
while True:
	dmesg = subprocess.Popen(['dmesg -T -l info'], stdout=subprocess.PIPE, shell=True) # -T shows human readable time
	(out, err) = dmesg.communicate()


	relevent_logs = []
	#parse dmesg output to a list of single logs
	dmesg_log = out.split('\n')
	new_tail = len(dmesg_log)
	dmesg_log = dmesg_log[tail-1:]                ########This is for not reading the same lines over and over.. instead of deleting the logs, we just skip them
	#print 'From %d to the end' % (tail-1)        ########Do not print anything! It's a standalone component!
	tail=new_tail
	
	#get all logs relevent to our module
	for line in dmesg_log:
		if MODULE_SIGNATURE in line:
			post_cut = line[line.find(']') + 2:]
			time = line[line.find('['):line.find(']')+1]
			relevent_logs.append('%s-%s' % (post_cut[len(MODULE_SIGNATURE):],time)) #The message is first because the time will destory the next section of slicing the logs by components

	for log in relevent_logs:
		if FIREWALL_ARP in log:
			logs_by_affiliation[ARP_KEY].append(log[len(FIREWALL_ARP):])

		elif FIREWALL_DOS in log:
			logs_by_affiliation[DOS_KEY].append(log[len(FIREWALL_DOS):])

		elif FIREWALL_RDHCP in log:
			logs_by_affiliation[RDHCP_KEY].append(log[len(FIREWALL_RDHCP):])
			
		elif FIREWALL_MISC in log:
			logs_by_affiliation[MISC_KEY].append(log[len(FIREWALL_MISC):])

		elif SYSCALL_HOOKING_MANAGER in log:
			logs_by_affiliation[SHM_MANAGER_KEY].append(log[len(SYSCALL_HOOKING_MANAGER):])

		elif SYSCALL_HOOKING_FILES in log:
			logs_by_affiliation[SHM_FILES_KEY].append(log[len(SYSCALL_HOOKING_FILES):])

		elif SYSCALL_HOOKING_SOCKETS in log:
			logs_by_affiliation[SHM_SOCKETS_KEY].append(log[len(SYSCALL_HOOKING_SOCKETS):])

		elif SYSCALL_HOOKING_DIRS in log:
			logs_by_affiliation[SHM_DIRS_KEY].append(log[len(SYSCALL_HOOKING_DIRS):])

		elif SYSCALL_HOOKING_PERMISSIONS in log:
			logs_by_affiliation[SHM_PERMISSIONS_KEY].append(log[len(SYSCALL_HOOKING_PERMISSIONS):])

		elif SYSCALL_HOOKING_FDS in log:
			logs_by_affiliation[SHM_FDS_KEY].append(log[len(SYSCALL_HOOKING_FDS):])

		elif SYSCALL_HOOKING_EXECUTIONS in log:
			logs_by_affiliation[SHM_EXECUTIONS_KEY].append(log[len(SYSCALL_HOOKING_EXECUTIONS):])
                elif FIREWALL_BLACKLIST in log:
			logs_by_affiliation[BLACKLIST_KEY].append(log[len(FIREWALL_BLACKLIST):])
                


	for key, log in logs_by_affiliation.iteritems():
		str = ''
		for line in log:
			str += line + '\n'

		if not os.path.exists(LOGS_DIR):
			os.system('mkdir ' + LOGS_DIR)

		with open(LOGS_DIR + '/' + key, 'a+') as f:
			f.write(str)

		# reset logs_by_affiliation
		logs_by_affiliation[key] = []

	
	sleep(NUMBER_OF_SECS_TO_SLEEP)
