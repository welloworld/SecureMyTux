#------------------Imports ----------------------#
import Tkinter as tk

import sys
sys.path.insert(0, 'tools/') #Import inside directory python codes

from subprocess import call
import pickle

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
dhcp_server = 'server_address'

class Globals(object):

	button_height = 4
	button_width = 18
	checkbutton_height = 3
	checkbutton_width = 30

	is_project_on = False
	# a dictionary containing which components of the project should run and what parameters to pass them
	project_components_info = {
		ARP: {power_state_on : True}#features_string_arg=A,fe_len=1
		,DOS: {power_state_on : True}#features_string_arg=D,fe_len=1
		,RDHCP: {power_state_on : False, dhcp_server: ''}#features_string_arg=R,fe_len=1 | dhcp_server_ip_arg="aaaa" server_len=4 //NOTICE: I think we changed aaaa addresses to 192.168.1.12 style
		,SHM: {power_state_on : True}
		,blacklist: {'addresses': '', 'length': 0}#blacklist_string_arg="192.168.1.12,11:22:33:44:55:dd,10.0.1.25" bl_len=3
		}


#-------------------------------- Run State Configuration ------------------------------#
STATE_CONF_FILE = '.project_run_configuration'#will be a .pkl file


#--------------------------------- Helper functions -------------------------------------#

class Manager(object):

	@staticmethod
	def load_state_conf():
		""" This function loads project-run configuration from 'STATE_CONF_FILE' into 'Globals.project_components_info' """
		with open(STATE_CONF_FILE, 'rb') as f:
			Globals.project_components_info = pickle.load(f)

	@staticmethod
	def save_state_conf():
		""" This function converts 'Globals.project_components_info' and saves it into 'STATE_CONF_FILE' """
		with open(STATE_CONF_FILE, 'wb') as f:
			pickle.dump(Globals.project_components_info, f, 1)#1 stands for backwards compatible pickling in binary

	@staticmethod
	def change_state_conf(conf):
		""" This function gets a dictionary with component names as keys and state changes as value.
		Example: {}"""
		pass

	@staticmethod
	def activate_project():
		""" This function activates the project with the current 'Globals.project_components_info' """
		firewall_activation = 'sudo insmod fw.ko '
		fw_param = {'features_string_arg':'', 'fe_len':0,'blacklist_string_arg':'', 'bl_len':0}
		shm_activation = './run_shm.sh'
		extra = ''

		#Activate Firewall
		if True == Globals.project_components_info[ARP][power_state_on]:
			fw_param['features_string_arg'] += 'A'
			fw_param['fe_len'] += 1
			
		elif True == Globals.project_components_info[DOS][power_state_on]:
			fw_param['features_string_arg'] += 'D'
			fw_param['fe_len'] += 1
			
		elif True == Globals.project_components_info[RDHCP][power_state_on]:
			fw_param['features_string_arg'] += 'R'
			fw_param['fe_len'] += 1
			extra = 'dhcp_server_ip_arg=' + Globals.project_components_info[RDHCP]['server_address'] + ' server_len=4' 
		
		#Run Firewall
		call(firewall_activation + 'features_string_arg='+fw_param['features_string_arg'] + ' fe_len='+str(fw_param['fe_len']) + ' blacklist_string_arg='+ Globals.project_components_info[blacklist]['addresses'] + ' bl_len='+ str(Globals.project_components_info[blacklist]['length']) + extra, shell = True)# rdhcp server ip parameters
		
		if Globals.project_components_info[SHM][power_state_on] == True:
			call(shm_activation, shell = True)
			
		Globals.is_project_on = True
			
	@staticmethod
	def clear_project():
		""" Shutdown project. remove Firewall and Syscall Hooking Manager. """
		fw_deactivation = 'sudo rmmod fw.ko'
		shm_deactivation = 'sudo rmmod shm.ko'
		
		#shutdown components
		call(shm_deactivation, shell = True)
		call(fw_deactivation, shell = True)
		
		Globals.is_project_on = False
			
	@staticmethod
	def restart_project():
		""" First clears project than starts it back on. Made for applying conf changes! """
		Manager.clear_project()
		Manager.activate_project()

		
