import subprocess

INFO_START = 2 #the command w has 2 header lines we need to skip

def is_not_empty(s):
    return (s != '')

	
def parse_w_output(out):
	""" This function gets the w shell command output and returns it parsed by lines and columns """
	parsed_output = []
	lines = filter(lambda x: is_not_empty(x),out.split('\n')[INFO_START:])
	for user in lines:
		data = filter(lambda x: is_not_empty(x),user.split(' '))
		parsed_output.append(data)
		
	return parsed_output
	
def printable_w_command_info(data):
	""" This function gets parsed data from w shell command and returns a print oriented string of it"""
	string = ''

	for line in data:
		string += 'User: %s' % (line[0])
		string += '\n'
		string += 'Terminal type: %s' % (line[1])
		string += '\n'
		string += 'Path to TTY for the user: %s' % (line[2])
		string += '\n'
		string += 'Last hard login from the user: %s' % (line[3])
		string += '\n'
		string += 'The user has been connected for: %s' % (line[4])
		string += '\n'
		string += 'Total time the CPU used by the user: %s' % (line[5])
		string += '\n'

	return string

	
def w_info():
	#run w shell command and get its info into 'out' variable
	dmesg = subprocess.Popen(['w'], stdout=subprocess.PIPE, shell=True)
	(out, err) = dmesg.communicate()

	data = parse_w_output(out)
	return printable_w_command_info(data)
	
