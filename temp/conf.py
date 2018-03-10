#------------------Imports ----------------------#
import Tkinter as tk

import sys
sys.path.insert(0, 'tools/') #Import inside directory python codes

from summarize_permissions import perms
from summarize_sudoers import sudoers_info
from logged_in import w_info
from ps_by_user import ps


#------------------------- Global Variables ---------------------------#
power_state_on = 'isOn'
DOS = 'dos'
ARP = 'arp'
RDHCP = 'rogue dhcp'
SHM = 'syscall hooking manager'
blacklist = 'blacklist'

class Globals(object):

	button_height = 4
	button_width = 18
	checkbutton_height = 3
	checkbutton_width = 30

	# a dictionary containing which components of the project should run and what parameters to pass them
	project_components_info = {
		ARP: {power_state_on : True}#features_string_arg=A,fe_len=1
		,DOS: {power_state_on : True}#features_string_arg=D,fe_len=1
		,RDHCP: {power_state_on : False, 'server_address': None}#features_string_arg=R,fe_len=1 | dhcp_server_ip_arg="aaaa" server_len=4 //NOTICE: I think we changed aaaa addresses to 192.168.1.12 style
		,SHM: {power_state_on : True}
		,blacklist: {'addresses': '', 'length': 0}#blacklist_string_arg="192.168.1.12,11:22:33:44:55:dd,10.0.1.25" bl_len=3
		}


#-------------------------------- Run State Configuration ------------------------------#
STATE_CONF_FILE = '.project_run_configuration'


#--------------------------------- Helper functions -------------------------------------#

class Manager(object):

	def load_state_conf():
	""" This function loads project-run configuration from 'STATE_CONF_FILE' into 'cur_run_state' """
	with open(STATE_CONF_FILE, 'r') as f:
		pass


	def save_state_conf():
		""" This function converts 'cur_run_state' and saves it into 'STATE_CONF_FILE' """
		pass


	def change_state_conf(conf):
		""" This function gets a dictionary with component names as keys and state changes as value.
		Example: {}"""
		pass

	def activate_component():
		""" This function activates the project with the current 'project_components_info' """
		firewall_activation = './run_fw.sh'
		fw_param = {'features_string_arg':'', 'fe_len':0,}
		shm_activation = ['./run_shm.sh']


		for comp,info in project_components_info.items():
			if info[power_state_on] == True:
				if comp == ARP:
					fw_param['features_string_arg'] += 'A'
				elif comp == DOS:
					fw_param['features_string_arg'] += 'D'
				elif comp == RDHCP:
					fw_param['features_string_arg'] += 'R'


				elif comp == SHM:
					pass #make sure activate shm part

				elif comp == blacklist:
					pass

				 


