#!/usr/bin/python2
from conf import *
		
#fix gui layout
#add functionality
class BlacklistScreen(object):
	
	def __init__(self, master):
		self.master = master
		self.master.title("Blacklist")

		self.frame = tk.Frame(master)
		
		address_input = tk.Text(self.frame, height = 5)
		address_input.grid(row = 0, column = 0)
		
		add_address_button = tk.Button(self.frame, text = 'Add address', command = self.add_address_callback, width = Globals.button_width, height = Globals.button_height)
		add_address_button.grid(row = 0, column = 1)
		
		delete_address_button = tk.Button(self.frame, text = 'Delete address', command = self.delete_address_callback, width = Globals.button_width, height = Globals.button_height)
		delete_address_button.grid(row = 1, column = 1)
		
		blacklist_view = tk.Text(self.frame, height = 20)
		blacklist_view.grid(row = 0, column = 2)
		
		self.frame.pack()
		
		
	def add_address_callback(self):
		""" This function is responsible for adding addresses to the blacklist """
		pass
	
	def delete_address_callback(self):
		""" This function is responsible for adding addresses to the blacklist """
		pass
	

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
		 'filename': {'on': tk.BooleanVar()} ,
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
		
		self.extra_input = tk.Entry(self.frame, text='Specific search', width=10)
		self.extra_input.grid(row = 0, column = 0, sticky='e')

		cur_column += 1

		self.show_button = tk.Button(self.frame, text = 'Show Logs', command = lambda: self.view_log_callback(), width = Globals.button_width, height = Globals.button_height)
		self.show_button.grid(row = 0, column = cur_column)
		cur_column += 1


		self.log_view = tk.Text(self.frame, height = 30)
		self.log_view.grid(row = 1, columnspan = cur_column)

		self.frame.pack()

	def view_log_callback(self):
		""" Uses self.params and functions from temp_logs_dividor.py to get info the user requested in self.params, than prints it to log_view """
		#global logs_data

		info = ''
		for key, settings in self.params.items():
			if settings['on'].get() == True:
				if self.extra_input.get() == '':
					info = get_all_kinds_of(key)
				else:
					info = search_in_logs(key, self.extra_input.get())

		if info == '':
			info = logs_data

		self.log_view.delete('1.0', tk.END)
		self.log_view.insert('1.0', info)


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
		Manager.clear_project(self)
		self.master.quit()
		self.master.destroy()

	def flip_switch_button(self):
		""" Changes the switch button to Off and On"""
		if Globals.is_project_on == True:
			self.project_state.set('Turn Off')
		else:
			self.project_state.set('Turn On')


def main():
	global main

	master = tk.Tk()
	Manager.load_state_conf()
	main = MainScreen(master)
	master.mainloop()
	"""
	perms(['1000'])
	sudoers_info()
	w_info()	
	ps('welloworld')
	"""
	


if __name__ == '__main__':
	main()
