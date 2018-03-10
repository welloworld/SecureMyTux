#!/usr/bin/python2
from conf import *
		

class BlacklistScreen(tk.Tk):
	
	def __init__(self):
		tk.Tk.__init__(self)
		
		address_input = tk.Text(self, height = 5)
		address_input.grid(row = 0, column = 0)
		
		add_address_button = tk.Button(self, text = 'Add address', command = self.add_address_callback, width = Globals.button_width, height = Globals.button_height)
		add_address_button.grid(row = 0, column = 1)
		
		delete_address_button = tk.Button(self, text = 'Delete address', command = self.delete_address_callback, width = Globals.button_width, height = Globals.button_height)
		delete_address_button.grid(row = 1, column = 1)
		
		blacklist_view = tk.Text(self, height = 20)
		blacklist_view.grid(row = 0, column = 2)
		
		
	def add_address_callback(self):
		""" This function is responsible for adding addresses to the blacklist """
		pass
	
	def delete_address_callback(self):
		""" This function is responsible for adding addresses to the blacklist """
		pass
	
	def exit(self):
		self.destroy()
		self.quit()
	
	
class ViewLogsScreen(tk.Tk):

	def __init__(self):
		tk.Tk.__init__(self)

		cur_column = 0
		# create view logs buttons in screen
		for component_name in Globals.project_components_info:
			view_log_button = tk.Button(self, text = component_name, command = self.show_log_callback, width = Globals.button_width, height = Globals.button_height)
			view_log_button.grid(row = 0, column = cur_column)
			cur_column += 1

		log_view = tk.Text(self, height = 20)
		log_view.grid(row = 1)


	def show_log_callback(self):
		""" This function is responsible for showing the requested log """
		pass
		
	def exit(self):
		self.destroy()
		self.quit()


class FeatureControlScreen(tk.Tk):

	def __init__(self):
		tk.Tk.__init__(self)

		cur_row = 0
		# create a switch button for each component
		for component_name in Globals.project_components_info:
			state = tk.Checkbutton(self, text = component_name, variable = tk.BooleanVar(), \
				onvalue = True, offvalue = False, height = Globals.checkbutton_height, width = Globals.checkbutton_width)
			state.grid(row = cur_row, column = 0, sticky = tk.W)
			cur_row += 1

		# create save button in screen
		save_button = tk.Button(self, text = 'Save changes', command = self.save_callback, width = Globals.button_width, height = Globals.button_height)
		save_button.grid(row = cur_row, column = 0)
		cur_row += 1
		# create edit blacklist button in screen
		edit_blacklist_button = tk.Button(self, text = 'Edit blacklist', command = self.switch_to_edit_blacklist_screen, width = Globals.button_width, height = Globals.button_height)
		edit_blacklist_button.grid(row = cur_row, column = 0)

	def save_callback(self):
		""" This function saves changes made to the components state """
		pass

	def switch_to_edit_blacklist_screen(self):
		""" This function is responsible for the functionality of Turn On\Off button """
		BlacklistScreen().mainloop()

	def exit(self):
		self.destroy()
		self.quit()		


class MainScreen(tk.Tk):
	""" Represents the first screen in the GUI. The general menu. """
	def __init__(self):
		tk.Tk.__init__(self)
		self.screens = []
		# create Turn On\Off button in screen
		switch_button = tk.Button(self, text = 'Turn On\Turn Off', command = self.switch_callback, width = Globals.button_width, height = Globals.button_height)
		switch_button.grid(row = 0, column = 0)

		# create View Logs button in screen
		view_button = tk.Button(self, text = 'View Logs', command = self.switch_to_view_logs_screen, width = Globals.button_width, height = Globals.button_height)
		view_button.grid(row = 0, column = 1)

		# create Feature control button in screen
		control_button = tk.Button(self, text = 'Feature Control', command = self.switch_to_feature_control_screen, width = Globals.button_width, height = Globals.button_height)
		control_button.grid(row = 1, column = 0)

		# create exit button in screen
		exit_button = tk.Button(self, text = 'Exit', command = self.exit_callback, width = Globals.button_width, height = Globals.button_height)
		exit_button.grid(row = 1, column = 1)


	def switch_callback(self):
		""" This function is responsible for the functionality of Turn On\Off button """
		pass

	def switch_to_view_logs_screen(self):
		""" This function is responsible for opening/switching to the view logs screen """
		s = ViewLogsScreen()
		self.screens.append(s)
		s.mainloop()

	def switch_to_feature_control_screen(self):
		""" This function is responsible for opening/switching to the view logs screen """
		s = FeatureControlScreen()
		self.screens.append(s)
		s.mainloop()
		
	def exit_callback(self):
		""" This function is callback to an exit attempt by the user """
		for s in self.screens:
			try:
				s.exit()
			except:
				pass
			
		self.destroy()
		self.quit()


def main():

	MainScreen().mainloop()
	"""
	perms(['1000'])
	sudoers_info()
	w_info()	
	ps('welloworld')
	"""
	
	


if __name__ == '__main__':
	main()
