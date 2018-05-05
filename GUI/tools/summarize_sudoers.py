import subprocess

def sudoers_info():
	""" This program runs a bash command to get the users who belong to the sudo group and returns the result """
	bash_to_extract_sudoers = 'getent group sudo | cut -d: -f4'

	res = subprocess.Popen([bash_to_extract_sudoers], stdout=subprocess.PIPE, shell=True)
	(out, err) = res.communicate()
	return 'The users who can run sudo permissions are:\n' + out