import subprocess
import re

def get_pair_value(data):
	""" Gets a pair string: name=value, and returns the value """
	return data.split('=')[1]


def split_to_strings(data):
	""" Gets a string made of words and signs and return a splited list of words in that string"""
	return re.findall('[a-zA-Z]+', data)
        

def printable_list(data):
	""" Get a list and print it """
	s = ''

	for val in data:
		s += val + '\n'

	return s


def perms(users):

	res = ''

	for user in users:
		#get info about user with the bash 'id' command
		dmesg = subprocess.Popen(['id ' + user], stdout=subprocess.PIPE, shell=True)
		(out, err) = dmesg.communicate()
		name, gid, groups = out.replace('\n','').split(' ')#split the id result into uid, gid, groups
	    
		# print the information
		res += '[***]USERNAME:'
		names = split_to_strings(get_pair_value(name))
		res += printable_list(names)

		res += '[***]GID:'
		gids = split_to_strings(get_pair_value(gid))
		res += printable_list(gids)

		res += '[***]Groups:'
		groups_list = split_to_strings(get_pair_value(groups))
		res += printable_list(groups_list).replace('\n', ',')[:-1]
		res += '\n\n'

	return res