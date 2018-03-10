import subprocess

 #Ps only prints the first 7 characters of the username so this function is used to search for a username we want.
def get_shortened_username(s):
	""" This function shortens a string which is supposedly a username into 7 chars long """
	if(len(s) > 7):
		return s[:7]
	return s	
	

def is_not_empty(s):
    return (s != '')

	
def parse_ps_output(out):
	""" This function gets the ps shell command output and returns it parsed by lines and columns """
	parsed_output = []
	lines = filter(lambda x: is_not_empty(x),out.split('\n'))
	for process in lines:
		data = filter(lambda x: is_not_empty(x),process.split(' '))
		parsed_output.append(data)
		
	return parsed_output
	
	
def print_ps_command_info(data):
	""" This function gets parsed data from ps shell command and prints it"""
	for line in data:
		print 'PID: %s' % (line[1])
		print 'Percentage of the CPU: %s' % (line[2])
		print 'Stat of process: %s' % (line[7])
		print 'Start time of the process: %s' % (line[8])
		print 'Running time of the process: %s' % (line[9])
		print 'The command itself: %s' % (' '.join(line[10:]))
		print '*****************************************************'

	
def ps(username):

	#run ps shell command and get its info for specific user into 'out' variable
	dmesg = subprocess.Popen(['ps -aux | grep "^' + get_shortened_username(username) + '"'], stdout=subprocess.PIPE, shell=True)#Are you sure we want ps -aux? probably dont need all processes
	(out, err) = dmesg.communicate()

	data = parse_ps_output(out)
	print_ps_command_info(data)

	