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
	
def print_w_command_info(data):
	""" This function gets parsed data from w shell command and prints it"""
	for line in data:
		print 'User: %s' % (line[0])
		print 'Terminal type: %s' % (line[1])
		print 'Path to TTY for the user: %s' % (line[2])
		print 'Last hard login from the user: %s' % (line[3])
		print 'The user has been connected for: %s' % (line[4])
		print 'Total time the CPU used by the user: %s' % (line[5])

	
def w_info():
	#run w shell command and get its info into 'out' variable
	dmesg = subprocess.Popen(['w'], stdout=subprocess.PIPE, shell=True)
	(out, err) = dmesg.communicate()

	data = parse_w_output(out)
	print_w_command_info(data)
	
