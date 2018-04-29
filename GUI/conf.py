#------------------Imports ----------------------#
import Tkinter as tk
from Tkinter import Label
import sys
sys.path.insert(0, 'tools/') #Import inside directory python codes

import subprocess
from subprocess import Popen
from subprocess import call

import pickle
import os
import re
import signal
from datetime import datetime

from time import strptime as time_strptime
import threading
import time

from summarize_permissions import perms
from summarize_sudoers import sudoers_info
from logged_in import w_info
from ps_by_user import ps
#from temp_logs_dividor import read_logs, search_in_logs, get_all_kinds_of, get_all_logs_by_date, delete_all_logs, logs_data


#------------------------- Global Variables ---------------------------#
power_state_on = 'isOn'
DOS = 'DOS Detector'
ARP = 'ARP Spoofing'
RDHCP = 'Rogue DHCP Detector'
SHM = 'Syscall Hooking Manager'
blacklist = 'blacklist'
dhcp_server = 'server_address'
sudoPassword = ''
CHARACTERS_IN_LINE = 80
RUN_EVERY = 30
logs_data = {}
subcategories_name_to_description = { #Don't worry about the lower and the uppercase - the code changes it to lowercase anyway 
    'FW_ARP' : 'ARP Spoofing',
    'FW_DHCP': 'Rouge DHCP',
    'FW_DOS' : 'DOS',
    'FW_MISC': 'Misc',
    'SHM_SC' : 'File descriptors',
    'SHM_SD' : 'Directories',
    'SHM_SE' : 'Executions',
    'SHM_SF' : 'Files',
    'SHM_SH' : 'Manager',
    'SHM_SP' : 'Permissions',
    'SHM_SS' : 'Sockets'
}

def runCommand(command):
    global sudoPassword
    Popen(['echo %s | sudo -S %s' % (sudoPassword, command)], shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)

class Globals(object):

	button_height = 4
	button_width = 18
	checkbutton_height = 3
	checkbutton_width = 20

	is_project_on = False
	# a dictionary containing which components of the project should run and what parameters to pass them
	project_components_info = {
		ARP: {power_state_on : True}#features_string_arg=A,fe_len=1
		,DOS: {power_state_on : True}#features_string_arg=D,fe_len=1
		,RDHCP: {power_state_on : False, dhcp_server: ''}#features_string_arg=R,fe_len=1 | dhcp_server_ip_arg="aaaa" server_len=4 //NOTICE: I think we changed aaaa addresses to 192.168.1.12 style
		,SHM: {power_state_on : True}
		,blacklist: {'addresses': [], 'length': 0}#blacklist_string_arg="192.168.1.12,11:22:33:44:55:dd,10.0.1.25" bl_len=3
		}

	# used in ViewLogsScreen in order to let the user choose users
	selected_users = {}


#-------------------------------- Run State Configuration ------------------------------#
STATE_CONF_FILE = '.project_run_configuration'#will be a .pkl file


#--------------------------------- Helper functions -------------------------------------#

class Manager(object):

	@staticmethod
	def load_state_conf():
		""" This function loads project-run configuration from 'STATE_CONF_FILE' into 'Globals.project_components_info' """
                try:
                    with open(STATE_CONF_FILE, 'rb') as f:
		    			Globals.project_components_info = pickle.load(f) #tab?
                except:
                    open(STATE_CONF_FILE, 'w').close()
                    
	@staticmethod
	def save_state_conf():
		""" This function converts 'Globals.project_components_info' and saves it into 'STATE_CONF_FILE' """
		with open(STATE_CONF_FILE, 'wb') as f:
			pickle.dump(Globals.project_components_info, f, 1)#1 stands for backwards compatible pickling in binary

	@staticmethod
	def activate_project(main_window):
		""" This function activates the project with the current 'Globals.project_components_info' """
		firewall_activation = 'insmod fw.ko '
		fw_param = {'features_string_arg':'', 'fe_len':0,'blacklist_string_arg':'', 'bl_len':0}
		shm_activation = './run_shm.sh'
		extra = ''

		#Activate Firewall
		if True == Globals.project_components_info[ARP][power_state_on]:
			fw_param['features_string_arg'] += 'A'
			fw_param['fe_len'] += 1
			print '[+++] ARP Spoofing added'
			
		if True == Globals.project_components_info[DOS][power_state_on]:
                    	fw_param['features_string_arg'] += 'D'
			fw_param['fe_len'] += 1
			print '[+++] DOS added'

		if True == Globals.project_components_info[RDHCP][power_state_on]:
			fw_param['features_string_arg'] += 'R'
			fw_param['fe_len'] += 1
			extra = 'dhcp_server_ip_arg=' + Globals.project_components_info[RDHCP]['server_address'] + ' server_len=' + str(len(Globals.project_components_info[RDHCP]['server_address']))
			print '[+++] RDHCP added'
		
		#Run Firewall
		command = firewall_activation + 'features_string_arg='+fw_param['features_string_arg'] + ' fe_len='+str(fw_param['fe_len']) + ' blacklist_string_arg='+ '.,'.join(Globals.project_components_info[blacklist]['addresses']) + '.,' + ' bl_len='+ str(len('.,'.join(Globals.project_components_info[blacklist]['addresses']))+2) + ' ' + extra
		
                print command
		runCommand(command)
                print '[+++] Firewall added'

		if Globals.project_components_info[SHM][power_state_on] == True:
			command = shm_activation
                        runCommand(command)
		print '[+++] Sys_hook_manager added'
		
                Globals.is_project_on = True
		main_window.flip_switch_button()
			
	@staticmethod
	def clear_project(main_window):
		""" Shutdown project. remove Firewall and Syscall Hooking Manager. """
		fw_deactivation = 'rmmod fw.ko'
		shm_deactivation = 'rmmod shm.ko'
		
		if Globals.is_project_on == True:
		    #shutdown components
		    command = fw_deactivation
		    runCommand(command)
                    print '[---] Firewall removed'
		    if Globals.project_components_info[SHM][power_state_on] == True:
		    	command = shm_deactivation
		    	runCommand(command)
                        print '[---] Sys_hook_manager removed'
		
		Globals.is_project_on = False
		main_window.flip_switch_button()
			
	@staticmethod
	def restart_project(main_window):
		""" First clears project than starts it back on. Made for applying conf changes! """
		if Globals.is_project_on == True:
			Manager.clear_project(main_window)
			Manager.activate_project(main_window)

		
