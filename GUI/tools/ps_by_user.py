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
	
	
def printable_ps_command_info(data):
	""" This function gets parsed data from ps shell command and returns a printable version of it"""
	s = ''

	for line in data:
		s += 'PID: %s' % (line[1]) + '\n'
		s += 'Percentage of the CPU: %s' % (line[2]) + '\n'
		s += 'Stat of process: %s' % (line[7]) + '\n'
		s += 'Start time of the process: %s' % (line[8]) + '\n'
		s += 'Running time of the process: %s' % (line[9]) + '\n'
		s += 'The command itself: %s' % (' '.join(line[10:])) + '\n'
		s += '*****************************************************' + '\n'

	return s

	
def ps(usernames):

	string = ''

	for username in usernames:
		#run ps shell command and get its info for specific user into 'out' variable
		dmesg = subprocess.Popen(['ps -aux | grep "^' + get_shortened_username(username) + '"'], stdout=subprocess.PIPE, shell=True)#Are you sure we want ps -aux? probably dont need all processes
		(out, err) = dmesg.communicate()

		data = parse_ps_output(out)
		string += printable_ps_command_info(data)

	return string
	