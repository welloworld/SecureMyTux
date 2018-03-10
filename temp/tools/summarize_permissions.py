import subprocess
import re

def get_pair_value(data):
	""" Gets a pair string: name=value, and returns the value """
	return data.split('=')[1]


def split_to_strings(data):
	""" Gets a string made of words and signs and return a splited list of words in that string"""
	return re.findall('[a-zA-Z]+', data)
        

def print_list(data):
	""" Get a list and print it """
	for val in data:
		print val


def perms(users):

	for user in users:
		#get info about user with the bash 'id' command
		dmesg = subprocess.Popen(['id ' + user], stdout=subprocess.PIPE, shell=True)
		(out, err) = dmesg.communicate()
		name, gid, groups = out.replace('\n','').split(' ')#split the id result into uid, gid, groups
	    
		# print the information
		print '[***]USERNAME:'
		names = split_to_strings(get_pair_value(name))
		print_list(names)

		print '[***]GID:'
		gids = split_to_strings(get_pair_value(gid))
		print_list(gids)

		print '[***]Groups:'
		groups_list = split_to_strings(get_pair_value(groups))
		print_list(groups_list)
		print