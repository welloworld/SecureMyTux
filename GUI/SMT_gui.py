#!/usr/bin/python2
from conf import *

#This class represents the Edit Blacklist screen which lets the user edit the blacklist (add, delete, and view records)
class BlacklistScreen(object):
	

	def __init__(self, master):
		''' This function initializes the blacklist screen with title and widgets.'''
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
		""" This function is responsible for adding addresses to the blacklist (adds the address written in the input field on the screen.
		After addition will refresh blacklist text box. """
		address = self.address_input.get()
		print Globals.project_components_info[blacklist]['addresses']
		print Globals.project_components_info[blacklist]['length']	
		if (not address in Globals.project_components_info[blacklist]['addresses'] and (is_mac(address) or is_ip(address))):
			#print 'good'
			Globals.project_components_info[blacklist]['addresses'].append(address)
                        Globals.project_components_info[blacklist]['length'] += len(address)
		print Globals.project_components_info[blacklist]['addresses']
		print Globals.project_components_info[blacklist]['length']		
		#else:
			#print 'notgood'	
		self.show_blacklist()

	def delete_address_callback(self):
		''' This function is responsible for deleting addresses from the blacklist (deletes the address written in the input field on the screen).
		After deleting the address will refresh the blacklist text box. '''

		#old = Globals.project_components_info[blacklist]['addresses'][:]
		Globals.project_components_info[blacklist]['addresses'] = filter(lambda x: x != self.address_input.get() , Globals.project_components_info[blacklist]['addresses'])
		#if old != Globals.project_components_info[blacklist]['addresses']:
			#Globals.project_components_info[blacklist]['length'] -= len(address)
		print Globals.project_components_info[blacklist]['addresses']
		print Globals.project_components_info[blacklist]['length']	
		self.show_blacklist()

	def show_blacklist(self):
		""" Print the blacklist into the Text widget """
		self.blacklist_view.delete('1.0', tk.END)
		for a in Globals.project_components_info[blacklist]['addresses']:
			self.blacklist_view.insert(tk.INSERT, a + '\n')

	def exit(self):
		''' Close the screen '''
		self.master.destroy()

# This class opens a screen which shows the user all of the existing users on the system and lets him choose by checking a checkbox which users he is interested in
class SelectUsersScreen(object):
	
	def __init__(self, master):
		self.master = master
		self.master.title("Select Users")

		self.frame = tk.Frame(master)
		# get all of the existing usernames
		dmesg = subprocess.Popen(['getent passwd | cut -d : -f 1'], stdout=subprocess.PIPE, shell=True)
		(out, err) = dmesg.communicate()

		cur_column = 0
		cur_row = 0
		# create a checkbutton for each username
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

# This class represents a screen which allows the user to watch and search the SMT logs.
class SmtLogsScreen(object):

	def __init__(self, master):
		''' Initialize the screen with the widgets '''
		self.master = master
		self.master.title("SMT Logs")

		self.frame = tk.Frame(self.master)

		self.options = ['Show all','uid','pid','mac','ip','syscall_name','path','subcategory']#,'date']

		cur_column = 0
		# Create the sort menu
		self.menuText = tk.StringVar()
		self.menuText.set(self.options[0])
		mb = tk.OptionMenu( self.frame, self.menuText, *self.options)
		mb.grid(row = 0, column = cur_column)

		cur_column += 1
		# Create the search input field
		self.extra_input = tk.Entry(self.frame, text='Specific search', width=15)
		self.extra_input.grid(row = 0, column = cur_column)

		cur_column += 1
		# Create show logs button
		self.show_button = tk.Button(self.frame, text = 'Show Logs', command = lambda: self.view_log_callback(), width = Globals.button_width, height = Globals.button_height)
		self.show_button.grid(row = 0, column = cur_column)
		cur_column += 1

		# Create delete logs button
		self.delete_button = tk.Button(self.frame, text = 'Delete ALL Logs', command = delete_all_logs, width = Globals.button_width, height = Globals.button_height)
		self.delete_button.grid(row = 0, column = cur_column)
		cur_column += 1

		# Create text box which will contain the logs
		self.log_view = tk.Text(self.frame, height = 30)
		self.log_view.grid(row = 1, columnspan = cur_column)

		self.frame.pack()

	def view_log_callback(self):
		""" Uses self.params and some other functions to get info the user requested in self.params, than prints it to log_view """
		global logs_data, CHARACTERS_IN_LINE
                
		info = ''
		mes=''

		if self.menuText.get() == 'Show all':# No sorting just display all logs
			info = logs_data
			if type(info) == dict:
				for k,v in info.items():
					mes += k + ' ( ~ %d Logs )' % (len(v)) + ':\n'
					mes += getLogsAsStr(v)
					mes = mes[:-1] + '\n'
		else:# Sort option chosen
			if self.extra_input.get() == '':# Sort option without special input
				info = get_all_kinds_of(self.menuText.get())
				for l in info:
					mes += str(l) + '\n'
			else:# Sort option with special input
				info = search_in_logs(self.menuText.get(), self.extra_input.get()) #info is a list that contains dicts of logs by the key and value.
				mes = getLogsAsStr(info)

		#i=0
		#for j in logs_data.values():
                #    i+=len(j)
		#print str(i)	
		self.log_view.delete('1.0', tk.END)
		self.log_view.insert('1.0', mes)

	def exit(self):
		self.master.destroy()

# This function converts logs dictionary into string
def getLogsAsStr(info):

    global CHARACTERS_IN_LINE
    mes = ''

    t_list = []
    for l in info: #For log in list of log
        temp=''
        for kk,vv in l.items(): #For key,value in the log
            temp += kk + ' = '
            if kk == 'date':
                vv = '%s/%s/%s %s:%s:%s' % (vv['day'],vv['month'],vv['year'],vv['hour'],vv['min'],vv['sec'])
            temp += vv + '\n\t'
        t_list.append(temp[:-1])
            
    last=[]
    for i in t_list:
        if not i in last:
            last.append(i)
    
    for count,i in enumerate(last):
        n = ' # %d # ' % (count)
        seperator = '-' * (CHARACTERS_IN_LINE/2) + n + '-' * (CHARACTERS_IN_LINE/2 -len(n)) + '\n\t'
        mes += seperator + i

    return mes

# This class represents a screen with buttons to show information like logged in users, who can use sudo, what permissions users has, and user processes history
class ExtraInfoScreen(object):

	def __init__(self, master):
		''' Initializes screen with widgets '''
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
		""" This function prints the result of the func parameter into the log text box. """
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
		""" Creates a screen to let the user choose which users he is interested in and return his choice"""
		s = tk.Toplevel(self.master)
		SelectUsersScreen(s)
		self.master.wait_window(s)
		return filter(lambda x: Globals.selected_users[x].get() == True, Globals.selected_users)

	def exit(self):
		""" Close the screen """
		self.master.destroy()

# This class represents a screen which lets the user change the on/off settings of components in the project and edit the blacklist
class FeatureControlScreen(object):

	state_buttons = []
	
	def __init__(self, master):
		''' Initialize the screen and widgets '''
		self.master = master
		self.master.title("Features Control")
		self.frame = tk.Frame(master)

		cur_row = 0
		# create a check button for each component
		for component_name, info in filter(lambda x: x[0] != blacklist, Globals.project_components_info.items()):
			var = tk.BooleanVar()
			self.state_buttons.append([component_name, var])
			state = tk.Checkbutton(self.frame, text = component_name, variable = self.state_buttons[-1][1], onvalue = 1, offvalue = 0, height = Globals.checkbutton_height, width = Globals.checkbutton_width)
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

		cur_row += 1
		self.dhcp_error_text = tk.StringVar()
		dhcp_input_error_label = tk.Label(self.frame, textvariable = self.dhcp_error_text)
		dhcp_input_error_label.grid(row = cur_row)

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
		""" This function saves changes made to the components state then closes the screen. """
		#Commit changes to Globals.project_components_info
		global main
		close_window = True
		for name,state_var in self.state_buttons:
			Globals.project_components_info[name][power_state_on] = state_var.get()
		
		dhcp = self.addr_input.get()
		if is_ip(dhcp):
			Globals.project_components_info[RDHCP][dhcp_server] = dhcp
		else:
			Globals.project_components_info[RDHCP][dhcp_server] = ''
			if Globals.project_components_info[RDHCP][power_state_on] == True:
				close_window = False
			Globals.project_components_info[RDHCP][power_state_on] = False
			self.dhcp_error_text.set('Invalid ip address.')
		
		#saves the configuration 
		Manager.save_state_conf()
		
		if close_window:
		#Restarts the project with the new settings
			Manager.restart_project(main)
			self.master.destroy()

	def switch_to_edit_blacklist_screen(self):
		""" This function opens the EditBlacklist screen. """
		s = tk.Toplevel(self.master)
		BlacklistScreen(s)	

	def exit(self):
		""" Closes the screen """
		self.master.destroy()


class MainScreen(object):
	""" Represents the first screen in the GUI. The general menu. """

	def __init__(self, master):
		#preparation for functionality
		command = 'python2 ../Logger/Logger.py'
		self.logger = Popen(['echo %s | sudo -S %s' % (sudoPassword, command)], shell=True,stdin=None, stdout=None, stderr=None, close_fds=True, preexec_fn=os.setsid)
		print '[+++] Logger added'
		t = threading.Thread(target=readEveryNSeconds)
		t.start()
		Manager.load_state_conf()

		#boot main screen
		self.open_screens=[]
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
		self.logs_button = tk.Button(self.frame, text = 'SMT Logs', command = self.switch_to_smt_logs_screen, width = Globals.button_width, height = Globals.button_height)
		self.logs_button.grid(row = 0, column = 1)

		# create Extra Info button in screen
		self.info_button = tk.Button(self.frame, text = 'Extra Info', command = self.switch_to_extra_info_screen, width = Globals.button_width, height = Globals.button_height)
		self.info_button.grid(row = 0, column = 2)

		# create Feature control button in screen
		self.control_button = tk.Button(self.frame, text = 'Feature Control', command = self.switch_to_feature_control_screen, width = Globals.button_width, height = Globals.button_height)
		self.control_button.grid(row = 1, column = 0)

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
		sc = SmtLogsScreen(s)
		self.open_screens.append(sc)
		self.logs_button["state"] = "disabled" 
		self.master.wait_window(s)
		self.logs_button["state"] = "normal"
		self.open_screens.remove(sc)

	def switch_to_extra_info_screen(self):
		""" This function is responsible for opening/switching to the extra information screen """
		s = tk.Toplevel(self.master)
		sc = ExtraInfoScreen(s)
		self.open_screens.append(sc)
		self.info_button["state"] = "disabled" 
		self.master.wait_window(s)
		self.info_button["state"] = "normal"
		self.open_screens.remove(sc)

	def switch_to_feature_control_screen(self):
		""" This function is responsible for opening/switching to the view logs screen """
		s = tk.Toplevel(self.master)
		sc = FeatureControlScreen(s)
		self.open_screens.append(sc)
		self.control_button["state"] = "disabled" 
		self.master.wait_window(s)
		self.control_button["state"] = "normal"
		self.open_screens.remove(sc)
		
	def exit_callback(self):
		""" This function is callback to an exit attempt by the user """
		for x in self.open_screens:
			x.exit()

		Manager.save_state_conf()
		Manager.clear_project(self)

		self.master.quit()# will quit mainloop and than in main will close tkinter
		print '[---] GUI destroyed'

		#self.logger.kill()
                runCommand('''kill $(ps -aux | grep "Logger" | awk '{print $2}')''')
                #pid = os.getpgid(self.logger.pid)
                #print pid
                #os.killpg(pid , signal.SIGTERM)
		print '[---] Logger removed'

	def flip_switch_button(self):
		""" Changes the switch button to Off and On"""
		if Globals.is_project_on == True:
			self.project_state.set('Turn Off')
		else:
			self.project_state.set('Turn On')
	

def filter_command(c):
    """
    This function filters a bash command
    Input:
        command
    Output:
        Filtered command
    """
    not_filter = ['\\']
    filtered = ''
    print '(%s)' % (c)
    for i in c:
        if not i.isdigit() and not i.isalpha() and not i in not_filter:
            filtered += '\\' + i
        else:
            filtered += i
    print '(%s)' % (filtered)
    return filtered    


# This class represents a popup window which requests the sudo password and verifies its correctness for later use.
class SudoScreen(object):

	def __init__(self,master):
		self.master = master
		self.master.title("Secure My Tux")

		self.frame = tk.Frame(master)
		
		label = tk.Label(self.frame, text = 'Enter root password:')
		label.pack()
		
		self.entry = tk.Entry(self.frame)
		self.entry.pack()
		
		entry_button = tk.Button(self.frame, text = 'Enter', command = self.save_sudo_password)
		entry_button.pack()
		
		self.error_label = tk.Label(self.frame, text = 'Incorrect password. Please try again.')
		
		self.frame.pack()

		self.master.protocol("WM_DELETE_WINDOW", self.exit_callback)

	def save_sudo_password(self):
		''' This function check if the sudo password is correct. If so it closes the sudo screen and switches to the MainScreen.
		Otherwise shows invalid password error and wait for a new one. '''
		global sudoPassword
		isCorrect = True
		sudoPassword = self.entry.get()
		
                sudoPassword = filter_command(sudoPassword)
		#try password
		trial = Popen(['echo %s | sudo -S echo sucessful_login' % (sudoPassword)], shell=True,stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
		out,err = trial.communicate()
		if 'Sorry' in err:
			isCorrect = False
			sudoPassword = ''
		
		if isCorrect:
			self.frame.destroy()
			main = MainScreen(self.master)
		else:
			self.error_label.pack()

	def exit_callback(self):
		''' Close the screen '''
		self.master.quit()
		
		
def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def is_mac(s):
	if not s.count(':')==5:
		return False

	splited = s.split(':')

	for i in splited:
		try:
			val = int(i,16)
		except ValueError:
			return False	
		if not val > 0 or not val < 256:
			return False
	return True

def is_ip(s):
	if not s.count('.')==3:
		return False

	splited = s.split('.')

	for i in splited:
		if not i.isdigit() or not int(i) > 0 or not int(i) < 256:
			return False
	return True 

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
    ''' This function reads all of the module logs from /var/log/smt '''
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

#Gets a search key and returns all options
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

# Deletes all logs in /var/log/smt
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

contin = True
# uses read_logs and is_in_danger to read the logs every RUN_EVERY and logs if danger is detected 
def readEveryNSeconds():
    global RUN_EVERY,contin,logs_data
    if contin:

        read_logs()  
        print 'logs readed'
        attacks = is_in_danger()
        if attacks:
    	    print '[***] UNDER ATTACK:'
    	    for log in attacks:
                print '\t' + str(log)
        time.sleep(RUN_EVERY)
        readEveryNSeconds()
    else:
        sys.exit(0)
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
	global main,sudoPassword, contin
	global logger #used in start_main_screen
	sudoPassword = ''
	master = tk.Tk()

	# check if we have sudo permissions
	trial = Popen(['echo '' | sudo -S echo successful_login'], shell=True,stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
	out,err = trial.communicate()
	if 'Sorry' in err:
		SudoScreen(master)#get sudo password from user for permissions
	else:
		MainScreen(master)

	# Run gui
	master.mainloop()
	master.destroy()

	contin = False
	print '[###] Please wait until the program gets killed'
	command = 'rm /var/log/smt/*'
	runCommand(command)

if __name__ == '__main__':
	main()
