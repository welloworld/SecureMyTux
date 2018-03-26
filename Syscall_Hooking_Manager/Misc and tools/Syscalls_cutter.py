import sys

SYSCALL_NAME = 1 #Index of the name of the syscall for mapping
PARAMS = range(3,8) #Params from the DB
syscalls_data_by_name = {}
known_rets = { 
	'read':'ssize_t',
	'write':'ssize_t'
} #All syscalls that the return type is not 'int'


def read_database():
	try:
		f = open('Syscalls.csv','r') #Open the DB
		
	except Exception as e:
		print '[*]Must have the database of the system calls!!!'
		sys.exit()

	syscalls = f.readlines()
	f.close()
	return syscalls


def create_function(syscall):
	"""
	Example of write() system call:
	asmlinkage long (*original_write) (unsigned int fd, const char __user *buf,size_t count);
	asmlinkage long our_write(unsigned int fd, const char __user *buf,size_t count)
	{
		printk("sys_write Called\n");
		return original_write(fd,buf,count);
	}
	"""
	#The function returns an array : [0] - all declarations for the .h files
	#								 [1] - all implementations for the .c files
	global syscalls_data_by_name
	global known_rets

	if syscall in known_rets.keys():
		ret = known_rets[syscall]
	else:
		ret = 'int'

	syscall = 'sys_' + syscall
	
	try:
		curr_syscall = syscalls_data_by_name[syscall].split(',')
	except Exception as e:
		print '[*][*][*]No syscall such as ' + syscall
		print
		return ''
	
	changing,returning,params,named_params,declare = '','','','',''

	for i in PARAMS:
		if curr_syscall[i] == '-':
			break
		params += curr_syscall[i].replace(' __user','') +','
		named_params += params[params.rfind(' '):].replace('*','').replace('&','') #Put some more filters!
	named_params = named_params[:-1]
	params = params[:-1]
	
	declare = 'asmlinkage '+ret+' (*original_' + syscall + ') ('+params + ');\n'
	st = 'asmlinkage '+ret+' our_' + syscall + '(' +params +')'
	declare += st + ';\n'
	st += '\n{\n'
	st += '\tdmesg_shm("' + syscall +' Called\\n");\n'
	st += '\treturn original_' + syscall +'('+named_params+');\n'
	st += '}\n'

	base_of_change_syscall = 'sys_table[__NR_' + syscall[4:]+'] = (void*)'

	changing = base_of_change_syscall + 'our_' + syscall + ';\n'
	returning= base_of_change_syscall + 'original_' + syscall +';\n'

	calling = 'original_' + syscall + ' = sys_table[__NR_' + syscall[4:]+'];\n'
	return [declare,st,changing,returning,calling]



def main():
	global syscalls_data_by_name
	
	syscalls = read_database()
	
	# creates a dictionary of syscall_name: data about it
	for syscall in syscalls:
		tmp = syscall.split(',')
		syscalls_data_by_name[tmp[SYSCALL_NAME]] = ','.join(tmp)
	

	#create the syscalls functions by mapping their name to the function 'create_function()'
	syscalls_list = map(lambda x: create_function(x), ['read','write','socket','close',
											'dup','dup2','pipe','bind',
											'listen','rmdir','mkdir','chmod',
											'fchmodat','fchmod','unlinkat','unlink',
											'open','connect',
											'accept','execve','chown',
											'lchown','fchown','fchownat','openat'])
											
	h_lines,functions,changes,returns,calling = '','','','',''
	for i in syscalls_list:
		if i == '':
			continue
		h_lines += i[0] + '\n'#Headers
		functions += i[1] + '\n'#Code
		changes += i[2]
		returns += i[3]
		calling += i[4]

	print 'For the .h file:'
	print h_lines
	print 'Calling:'
	print calling
	print 'Syscall changes:'
	print changes
	print 'Syscall changing back:'
	print returns
	print 'Functions:'
	print functions

if __name__ == '__main__':
	main()

	