#!/usr/bin/python2
from conf import *
		

class BlacklistScreen(object):
	
	def __init__(self, master):
		self.master = master
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
	
	
class ViewLogsScreen(object):

	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(master)

		cur_column = 0
		# create view logs buttons in screen
		for component_name in Globals.project_components_info:
			view_log_button = tk.Button(self.frame, text = component_name, command = self.show_log_callback, width = Globals.button_width, height = Globals.button_height)
			view_log_button.grid(row = 0, column = cur_column)
			cur_column += 1

		log_view = tk.Text(self.frame, height = 20)
		log_view.grid(row = 1, columnspan = cur_column)

		self.frame.pack()

	def show_log_callback(self):
		""" This function is responsible for showing the requested log """
		pass


class FeatureControlScreen(object):

	state_buttons = []
	
	def __init__(self, master):
		self.master = master
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
			
		# create save button in screen
		save_button = tk.Button(self.frame, text = 'Save changes', command = self.save_callback, width = Globals.button_width, height = Globals.button_height)
		save_button.grid(row = cur_row, column = 0)
		cur_row += 1
		# create edit blacklist button in screen
		edit_blacklist_button = tk.Button(self.frame, text = 'Edit blacklist', command = self.switch_to_edit_blacklist_screen, width = Globals.button_width, height = Globals.button_height)
		edit_blacklist_button.grid(row = cur_row, column = 0)
		
		self.frame.pack()

	def save_callback(self):
		""" This function saves changes made to the components state """
		#TODO: commit changes to Globals.project_components_info
		for name,state_var in self.state_buttons:
			Globals.project_components_info[name][power_state_on] = state_var.get()
			print name, state_var.get()
		
		Manager.save_state_conf()
		#Manager.restart_project()

	def switch_to_edit_blacklist_screen(self):
		""" This function is responsible for the functionality of Turn On\Off button """
		s = tk.Toplevel(self.master)
		BlacklistScreen(s)	


class MainScreen(object):
	""" Represents the first screen in the GUI. The general menu. """
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(master)
		self.screens = []
		# create Turn On\Off button in screen
		switch_button = tk.Button(self.frame, text = 'Turn On\Turn Off', command = self.switch_callback, width = Globals.button_width, height = Globals.button_height)
		switch_button.grid(row = 0, column = 0)

		# create View Logs button in screen
		view_button = tk.Button(self.frame, text = 'View Logs', command = self.switch_to_view_logs_screen, width = Globals.button_width, height = Globals.button_height)
		view_button.grid(row = 0, column = 1)

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
			Manager.clear_project()
		else:
			Manager.activate_project()

	def switch_to_view_logs_screen(self):
		""" This function is responsible for opening/switching to the view logs screen """
		s = tk.Toplevel(self.master)
		ViewLogsScreen(s)

	def switch_to_feature_control_screen(self):
		""" This function is responsible for opening/switching to the view logs screen """
		s = tk.Toplevel(self.master)
		FeatureControlScreen(s)
		
	def exit_callback(self):
		""" This function is callback to an exit attempt by the user """
		self.master.quit()
		self.master.destroy()
		

def main():

	master = tk.Tk()
	Manager.load_state_conf()
	MainScreen(master)
	master.mainloop()
	"""
	perms(['1000'])
	sudoers_info()
	w_info()	
	ps('welloworld')
	"""
	


if __name__ == '__main__':
	main()
