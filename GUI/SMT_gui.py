#!/usr/bin/python2
from conf import *
	
#add functionality
class BlacklistScreen(object):
	
	def __init__(self, master):
		self.master = master
		self.master.title("Blacklist")

		self.frame = tk.Frame(master)
		
		self.blacklist_view = tk.Text(self.frame, height = 20, width = 20)
		self.blacklist_view.pack(side = tk.RIGHT)

		self.address_input = tk.Entry(self.frame)
		self.address_input.pack(side = tk.TOP)

		add_address_button = tk.Button(self.frame, text = 'Add address', command = self.add_address_callback, width = Globals.button_width, height = Globals.button_height)
		add_address_button.pack()

		delete_address_button = tk.Button(self.frame, text = 'Delete address', command = self.delete_address_callback, width = Globals.button_width, height = Globals.button_height)
		delete_address_button.pack()

		self.frame.pack()
		self.show_blacklist()
				
	def add_address_callback(self):
		""" This function is responsible for adding addresses to the blacklist """
		Globals.project_components_info[blacklist]['addresses'].append(self.address_input.get())
		Globals.project_components_info[blacklist]['length'] += 1
		self.show_blacklist()

	def delete_address_callback(self):
		""" This function is responsible for adding addresses to the blacklist """
		Globals.project_components_info[blacklist]['addresses'] = filter(lambda x: x != self.address_input.get() , Globals.project_components_info[blacklist]['addresses'])
		Globals.project_components_info[blacklist]['length'] -= 1
		self.show_blacklist()

	def show_blacklist(self):
		""" Print the blacklist """
		self.blacklist_view.delete('1.0', tk.END)
		for a in Globals.project_components_info[blacklist]['addresses']:
			self.blacklist_view.insert(tk.INSERT, a + '\n')


class SelectUsersScreen(object):
	
	def __init__(self, master):
		self.master = master
		self.master.title("Select Users")

		self.frame = tk.Frame(master)

		dmesg = subprocess.Popen(['getent passwd | cut -d : -f 1'], stdout=subprocess.PIPE, shell=True)
		(out, err) = dmesg.communicate()

		cur_column = 0
		cur_row = 0
		# create a switch button for each component
		for username in out.split('\n')[:-1]:
			var = tk.BooleanVar()
			Globals.selected_users[username] = var

			state = tk.Checkbutton(self.frame, text = username, variable = Globals.selected_users[username], 
				 onvalue = 1, offvalue = 0, height = Globals.checkbutton_height, width = Globals.checkbutton_width 
				)
			state.grid(row = cur_row, column = cur_column, sticky = tk.W)
			
			cur_column += 1
			if cur_column == 6:
				cur_row += 1
				cur_column = 0

		self.frame.pack()


class SmtLogsScreen(object):

	def __init__(self, master):
		self.master = master
		self.master.title("SMT Logs")

		self.frame = tk.Frame(self.master)

		self.params = {'uid': {'on': tk.BooleanVar()} ,
		 'pid': {'on': tk.BooleanVar()} ,
		 'mac': {'on': tk.BooleanVar()} ,
		 'ip': {'on': tk.BooleanVar()} ,
		 'syscall_name': {'on': tk.BooleanVar()} ,
		 'path': {'on': tk.BooleanVar()} ,
		 'subcategory': {'on': tk.BooleanVar()} ,
		 'date': {'on': tk.BooleanVar()}
		 }

		cur_column = 0
		menuText = tk.StringVar()
		menuText.set('Sort by:')
		mb = tk.Menubutton( self.frame, textvariable = menuText, relief = tk.RAISED)
		mb.grid(row = 0, column = 0)
		mb.menu = tk.Menu(mb, tearoff = 0)
		mb['menu'] = mb.menu

		for component_name, settings in self.params.items():
			mb.menu.add_checkbutton(label = component_name, variable = settings['on'])
		
		cur_column += 1

		self.extra_input = tk.Entry(self.frame, text='Specific search', width=15)
		self.extra_input.grid(row = 0, column = cur_column)

		cur_column += 1

		self.show_button = tk.Button(self.frame, text = 'Show Logs', command = lambda: self.view_log_callback(), width = Globals.button_width, height = Globals.button_height)
		self.show_button.grid(row = 0, column = cur_column)
		cur_column += 1

		self.delete_button = tk.Button(self.frame, text = 'Delete ALL Logs', command = delete_all_logs, width = Globals.button_width, height = Globals.button_height)
		self.delete_button.grid(row = 0, column = cur_column)
		cur_column += 1

		self.log_view = tk.Text(self.frame, height = 30)
		self.log_view.grid(row = 1, columnspan = cur_column)

		self.frame.pack()

	def view_log_callback(self):
		""" Uses self.params and functions from temp_logs_dividor.py to get info the user requested in self.params, than prints it to log_view """
		global logs_data

		info = ''
		mes=''
		f = False
		for key, settings in self.params.items():
			if settings['on'].get() == True:
				if self.extra_input.get() == '':
					#print key
					info = get_all_kinds_of(key)
					for l in info:
						mes += str(l) + '\n'
				else:

					info = search_in_logs(key, self.extra_input.get())
					for l in info:
						for kk,vv in l.items():
							mes += str(kk) + '=' + str(vv) + '\n\t'
						#mes = mes[:-1]	
						mes += '\n\t'

		if info == '':
			info = logs_data
			#print info
			if type(info) == dict:
				for k,v in info.items():
					mes += k +':\n\t'
					for l in v:
						for kk,vv in l.items():
							mes += str(kk) + '=' + str(vv) + '\n\t'
						#mes = mes[:-1]	
						mes += '\n\t'

					mes = mes[:-1] + '\n'
			

		i=0
		for j in logs_data.values():
			i+=len(j)
		#print str(i)	
		self.log_view.delete('1.0', tk.END)
		self.log_view.insert('1.0', mes)


class ExtraInfoScreen(object):

	def __init__(self, master):
		self.master = master
		self.master.title("Information")

		self.frame = tk.Frame(master)

		cur_column = 0
		# create information buttons in screen
		# Logged in users button
		logged_in_users_button = tk.Button(self.frame, text = 'Logged in users', command = lambda: self.view_log_callback(w_info), width = Globals.button_width, height = Globals.button_height)
		logged_in_users_button.grid(row = 0, column = cur_column)
		cur_column += 1

		# Sudoers group button
		sudoers_info_button = tk.Button(self.frame, text = 'Sudoers group', command = lambda: self.view_log_callback(sudoers_info), width = Globals.button_width, height = Globals.button_height)
		sudoers_info_button.grid(row = 0, column = cur_column)
		cur_column += 1		

		# Users permissions button
		users_permissions_button = tk.Button(self.frame, text = 'Users permissions', command = lambda: self.view_log_callback(perms, func_param = self.get_users_from_user()), width = Globals.button_width, height = Globals.button_height)
		users_permissions_button.grid(row = 0, column = cur_column)
		cur_column += 1

		# Processes view by users button
		users_processes_history_button = tk.Button(self.frame, text = 'User processes history', command = lambda: self.view_log_callback(ps, func_param = self.get_users_from_user()), width = Globals.button_width, height = Globals.button_height)
		users_processes_history_button.grid(row = 0, column = cur_column)
		cur_column += 1
		'''
		project_logs_button = tk.Button(self.frame, text = 'SMT Logs', command = lambda: self.view_log_callback(ps, func_param = self.get_users_from_user()), width = Globals.button_width, height = Globals.button_height)
		project_logs_button.grid(row = 0, column = cur_column)
		cur_column += 1
		'''
		self.log_view = tk.Text(self.frame, height = 30)
		#self.log_view = tk.LabelFrame(self.frame,height = 100)
		self.log_view.grid(row = 1, columnspan = cur_column)

		self.frame.pack()

	def view_log_callback(self, func, func_param = None):
		""" This function shows a log of all connected users """
		beginning = '1.0'# location to insert text
		self.log_view.delete(beginning, tk.END)
		if func_param == None:
			self.log_view.insert(beginning, func())
		else:
			self.log_view.insert(beginning, func(func_param))
		""" ############################ It works good but I can't find how to delete the old Labels
		try:
			self.label.destroy()
		except:
			pass
		self.log_view = tk.LabelFrame(self.frame,height = 100)
		self.log_view.grid(row = 1, columnspan = 10)
		#self.log_view.pack(fill="both",expand="yes")

		if func_param == None:
			self.label = Label(self.log_view,text=func())
			self.label.pack()
		else:
			self.label = Label(self.log_view,text=func(func_param))
			self.label.pack()
		self.log_view.pack()	
		"""
	def get_users_from_user(self):
		""" Let the user choose which users he is interested in and return his choice"""
		s = tk.Toplevel(self.master)
		SelectUsersScreen(s)
		self.master.wait_window(s)
		return filter(lambda x: Globals.selected_users[x].get() == True, Globals.selected_users)


class FeatureControlScreen(object):

	state_buttons = []
	
	def __init__(self, master):
		self.master = master
		self.master.title("Features Control")
		self.frame = tk.Frame(master)

		cur_row = 0
		# create a switch button for each component
		for component_name, info in filter(lambda x: x[0] != blacklist, Globals.project_components_info.items()):
			var = tk.BooleanVar()
			self.state_buttons.append([component_name, var])
			state = tk.Checkbutton(self.frame, text = component_name, variable = self.state_buttons[-1][1], 
				 onvalue = 1, offvalue = 0, height = Globals.checkbutton_height, width = Globals.checkbutton_width 
				)
			state.grid(row = cur_row, column = 0, sticky = tk.W)
			cur_row += 1
			
			if True == info[power_state_on]:
					state.toggle()#check button on
		
		t = tk.StringVar()
		t.set('DHCP server ip:')
		label = tk.Label(self.frame, textvariable = t)
		label.grid(row = cur_row, sticky = 'w')
		self.addr_input = tk.Entry(self.frame, width=10)
		self.addr_input.grid(row = cur_row, sticky = 'e')
		
		# create save button in screen
		cur_row += 1
		save_button = tk.Button(self.frame, text = 'Save changes', command = self.save_callback, width = Globals.button_width, height = Globals.button_height)
		save_button.grid(row = cur_row, column = 0)
		
		# create edit blacklist button in screen
		cur_row += 1
		edit_blacklist_button = tk.Button(self.frame, text = 'Edit blacklist', command = self.switch_to_edit_blacklist_screen, width = Globals.button_width, height = Globals.button_height)
		edit_blacklist_button.grid(row = cur_row, column = 0)
		
		self.frame.pack()

	def save_callback(self):
		""" This function saves changes made to the components state """
		#Commit changes to Globals.project_components_info
		for name,state_var in self.state_buttons:
			Globals.project_components_info[name][power_state_on] = state_var.get()
		
		Globals.project_components_info[RDHCP][dhcp_server] = self.addr_input.get()
		
		print Globals.project_components_info
		#saves the configuration 
		Manager.save_state_conf()
		
		#Restarts the project with the new settings
		Manager.restart_project(main)

	def switch_to_edit_blacklist_screen(self):
		""" This function is responsible for the functionality of Turn On\Off button """
		s = tk.Toplevel(self.master)
		BlacklistScreen(s)	


class MainScreen(object):
	""" Represents the first screen in the GUI. The general menu. """

	def __init__(self, master):
		self.master = master
		self.master.title("Secure My Tux")

		self.frame = tk.Frame(master)
		self.screens = []
		self.project_state = tk.StringVar()
		# create Turn On\Off button in screen
		self.project_state.set('Turn On')
		switch_button = tk.Button(self.frame, textvariable = self.project_state, command = self.switch_callback, width = Globals.button_width, height = Globals.button_height)
		switch_button.grid(row = 0, column = 0)

		# create SMT Logs button in screen
		logs_button = tk.Button(self.frame, text = 'SMT Logs', command = self.switch_to_smt_logs_screen, width = Globals.button_width, height = Globals.button_height)
		logs_button.grid(row = 0, column = 1)

		# create Extra Info button in screen
		info_button = tk.Button(self.frame, text = 'Extra Info', command = self.switch_to_extra_info_screen, width = Globals.button_width, height = Globals.button_height)
		info_button.grid(row = 0, column = 2)

		# create Feature control button in screen
		control_button = tk.Button(self.frame, text = 'Feature Control', command = self.switch_to_feature_control_screen, width = Globals.button_width, height = Globals.button_height)
		control_button.grid(row = 1, column = 0)

		# create exit button in screen
		exit_button = tk.Button(self.frame, text = 'Exit', command = self.exit_callback, width = Globals.button_width, height = Globals.button_height)
		exit_button.grid(row = 1, column = 1)
		self.frame.pack()

		self.master.protocol("WM_DELETE_WINDOW", self.exit_callback)

	def switch_callback(self):
		""" This function is responsible for the functionality of Turn On\Off button """
		if True == Globals.is_project_on:
			Manager.clear_project(self)
		else:
			Manager.activate_project(self)

	def switch_to_smt_logs_screen(self):
		""" Opens the smt logs screen """
		s = tk.Toplevel(self.master)
		SmtLogsScreen(s)

	def switch_to_extra_info_screen(self):
		""" This function is responsible for opening/switching to the extra information screen """
		s = tk.Toplevel(self.master)
		ExtraInfoScreen(s)

	def switch_to_feature_control_screen(self):
		""" This function is responsible for opening/switching to the view logs screen """
		s = tk.Toplevel(self.master)
		FeatureControlScreen(s)
		
	def exit_callback(self):
		""" This function is callback to an exit attempt by the user """
		Manager.save_state_conf()
		Manager.clear_project(self)

		self.master.quit()
		self.master.destroy()
		print 'BYE-BYE'

	def flip_switch_button(self):
		""" Changes the switch button to Off and On"""
		if Globals.is_project_on == True:
			self.project_state.set('Turn Off')
		else:
			self.project_state.set('Turn On')


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def is_ip(s):
    return (s.count('.') == 3) 

def replace_all(string,to_replace,what):
    for letter in to_replace:
        string = string.replace(letter,what)
    return string

def get_normal_date(d):
    date_splited = d.split(' ')
    #print date_splited
    #needed_date = '%s:%s:%s:%s' % (date_splited[3],str(time_strptime(date_splited[1],'%b').tm_mon), date_splited[5], date_splited[4])
    needed_date = '%s:%s:%s:%s' % (date_splited[2],str(time_strptime(date_splited[1],'%b').tm_mon), date_splited[4], date_splited[3])
    #needed_date looks like: '9-3-2018 11:22:03'
    perfect_date = {}
    needed_date_splitted = needed_date.split(':')

    perfect_date['day'] = needed_date_splitted[0]
    perfect_date['month'] = needed_date_splitted[1]
    perfect_date['year'] = needed_date_splitted[2]
    perfect_date['hour'] = needed_date_splitted[3]
    perfect_date['min'] = needed_date_splitted[4]
    perfect_date['sec'] = needed_date_splitted[5]


    return perfect_date
    

def log_contains_ip_or_mac(l):
    #droped [mac][ip]
    log_info = {}
    if '[' in l and ']' in l:
        for s in [m.start() for m in re.finditer('\[', l)]:
            ip_or_mac = l[s+1:l.find(']',s)]
            if is_ip(ip_or_mac):
                log_info['ip'] = ip_or_mac
            else:
                log_info['mac']= ip_or_mac
    return log_info                



def read_logs():
    global logs_data
    logs_data_temp={}
    smt_dir = '/var/log/smt'
    if os.path.exists(smt_dir):
        smt_files = os.listdir(smt_dir)
        
        if len(smt_files) == 0:
            print 'No files :('
        
        else:
            
            for fname in smt_files:
                
                f = open( smt_dir + '/' + fname,'r')
                lines = f.readlines()
                logs_data_temp[fname] = [line.replace('\n','').rsplit('-',1) for line in lines]
                
        for name,logs in logs_data_temp.items():
            #print logs_data_temp[fname]
            logs_data[name] = []
            sub =  subcategories_name_to_description[name] if name in subcategories_name_to_description else ''
            

            if name.startswith('SHM') and name[-1] != 'H':
                for log in logs:
                    
                    date = get_normal_date(replace_all(log[1],'[]',''))
                    syscall_params = log[0].split(':',1)
                    params_list = map(lambda x : x.strip(), syscall_params[1].split(' | ')) 
                    #print params_list
                    params_dic = {}
                    
                    #print params_list
                    for param in params_list:
                        key_val_param = param.split('=')
                        if len(key_val_param) > 1:
                            params_dic[key_val_param[0]] = key_val_param[1]
                    
                    log = {'syscall_name' : syscall_params[0],'date' : date , 'subcategory' : sub}
                    	
                    log = merge_two_dicts(log,params_dic)
                    #if 'address' in log:
                    #	print log
                    #else:
                    	#print log
                    logs_data[name].append(log)

            else:
                
                if name.startswith('FW'):
                    for log in logs:

                        date = get_normal_date(replace_all(log[1],'[]',''))
                        mes = log[0].split(':',1)[0]
                        
                        ip_and_mac = {'date' : date, 'message' : mes, 'subcategory' : sub}
                        log = merge_two_dicts(log_contains_ip_or_mac(log[0]),ip_and_mac)
                        #print log
                        logs_data[name].append(log)
                else:
                    for log in logs:
                        
                        date = get_normal_date(replace_all(log[1],'[]',''))
                        mes = log[0]

                        logs_data[name].append({'date' : date,'message' : mes,'subcategory' : sub})

                #else:
                #    print '%s is empty' % (name) #Actually need to read here the logs that not from the syscalls
    else:
        print '%s is not defined' % (smt_dir)
   
#This function searches inside the logs data, for example - get all logs with pid 1000 - you send 'pid' as key and 1000 as value.
#Works on every key (Go to supporting keys)
#Need to support date,subcategory
def search_in_logs(key,value):
    global logs_data
    ans = []
    for name,logs in logs_data.items():
        for log in logs:
            if key in log:
                if log[key].lower() == str(value).lower():
                    ans.append(log)
    return ans

def get_all_kinds_of(key):
    global logs_data
    all_types = []
    for name,logs in logs_data.items():
        for log in logs:
            if key in log and log[key] not in all_types:
                all_types.append(log[key])

    return all_types            

"""
time_part = { #any seconds in 10:39 on the 9-3-2018
        'sec' : '', 
        'min' : '39',
        'hour' :'10',
        'day' : '9',
        'month' : '3',
        'year' : '2018'
    }
"""
def get_all_logs_by_date(time_part):
    global logs_data
    all_types = []
    for name,logs in logs_data.items():
        for log in logs:
            d = log['date']
            ok=True
            for k,v in time_part.items():
                if v:  #Empty means no treatment
                    if k not in d or str(v) != str(d[k]):
                        ok = False
            if ok:
                all_types.append(log)
    return all_types                        

"""
1. Delete previous logs_data
2. Kill Logger
3. Delete all log files
4. Clear dmesg
5. Run Logger again
"""
def delete_all_logs():

    global logs_data,sudoPassword
    logs_data.clear()
    smt_dir = '/var/log/smt'
    
    if os.path.exists(smt_dir):
        smt_files = os.listdir(smt_dir)
        if len(smt_files) == 0:
            print 'No files :('
        else:
            for fname in smt_files:
                command = 'rm ' + smt_dir + '/' + fname
                os.system('echo %s | sudo -S %s' % (sudoPassword, command))

                #os.remove( smt_dir + '/' + fname)
            print 'All logs deleted'
    else:
        print '%s is not defined' % (smt_dir)


def is_in_danger(): #This function should be checked!
    global logs_data
    attacks=[]
    fw_logs = search_in_logs('subcategory','rogue dhcp') + search_in_logs('subcategory','arp spoofing') + search_in_logs('subcategory','dos')
    for log in fw_logs:
        if 'message' in log and 'Attack' in log['message'] and log['message'].count('{') == 1 and log['message'].count('}') == 1:
            attacks.append(log)

    if len(attacks) > 0:
        return attacks
    else:
        return None    


def readEveryNSeconds():
    global RUN_EVERY
    threading.Timer(RUN_EVERY, readEveryNSeconds).start()
    read_logs()  
    print 'logs readed'
    attacks = is_in_danger()
    if attacks:
    	print 'UNDER ATTACK:'
    	for log in attacks:
    		print '\t' + str(log)
    #print logs_data
    
readEveryNSeconds()     
#is_in_danger()
#print search_in_logs('subcategory','arp spoofing')
#print search_in_logs('date','09-03-2018 10:30') #Works on every key (Go to supporting keys)
#print logs_data
#print get_all_kinds_of('subcategory') #Works on every key (Go to supporting keys)
#print get_all_logs_by_date({'hour': '11', 'min': '22', 'month': '3', 'sec': '34', 'year': '2018', 'day': '9'})


"""
Supporting keys:
    * uid
    * pid
    * mac
    * ip
    * syscall_name
    * filename
    * subcategory
    * date - other function
"""

def main():
	global main
	global sudoPassword
	command = 'python2 Logger.py'
	
	logger = Popen(['echo %s | sudo -S %s' % (sudoPassword, command)], shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)
	print 'Logger runs'
	master = tk.Tk()
	Manager.load_state_conf()
	main = MainScreen(master)
	master.mainloop()
	logger.kill()
	print 'Logger killed'
	sys.exit(0)
	"""
	perms(['1000'])
	sudoers_info()
	w_info()	
	ps('welloworld')
	"""
	


if __name__ == '__main__':
	main()