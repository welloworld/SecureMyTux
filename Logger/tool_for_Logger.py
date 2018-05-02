defs = '''#define SYSCALL_HOOKING_MANAGER "[SH]"
#define SYSCALL_HOOKING_FILES "[SF]"
#define SYSCALL_HOOKING_SOCKETS "[SS]"
#define SYSCALL_HOOKING_DIRS "[SD]"
#define SYSCALL_HOOKING_PERMISSIONS "[SP]"
#define SYSCALL_HOOKING_FDS "[SC]" //OUT OF LETTES :(
#define SYSCALL_HOOKING_EXECUTIONS "[SE]"'''

print_function = '#define dmesg_~(fmt, ...) printk(KERN_INFO MODULE_SIGNATURE & pr_fmt(fmt), ##__VA_ARGS__)'
check_if_logger = 'elif ^ in log:\n\tlogs_by_affiliation[&].append(log[len(^):])'
"""
This function creates a function by C-define-conventions.
input:
    define string
Output:    
    function by the define
"""
def create_function(define):
	global print_function
	name = define.split(' ')[1]

	return print_function.replace('&',name).replace('~', 'shm_' + name.split('_')[2].lower())
"""
This function creates a logger definition.
input:
    define string
Output:    
    logger definition by the define
"""

def create_logger_def(define):
	value = define.split(' ')[2]
	name = define.split(' ')[1]

	return name + ' = ' + value.replace('\"','\'')

"""
This function creates a logger key by python-keys-conventions.
input:
    define string
Output:    
    logger-key by the define
"""

def create_logger_key(define):
	value = define.split(' ')[2]
	name = define.split(' ')[1]

	return 'SHM_' + name.split('_')[2] + '_KEY = \'SHM_' + value.replace('\"','').replace('[','').replace(']','') + '\''
"""
This function creates a logger-condition by python-condition-conventions.
input:
    define string
Output: 
    logger-condition by the define
"""

def create_logger_if(define):
	global check_if_logger
	name = define.split(' ')[1]
	key = 'SHM_' + name.split('_')[2] + '_KEY' 

	return check_if_logger.replace('^',name).replace('&',key)
"""
This function creates a logger-declaration by python-declaration-conventions.
input:
    define string
Output:    
    logger-declaration by the define
"""

def create_logger_decl(define):
	name = define.split(' ')[1]
	key = 'SHM_' + name.split('_')[2] + '_KEY' 

	return key + ': [],'
defs_l = defs.split('\n')

functions = map(lambda x: create_function(x),defs_l)
logger =    map(lambda x: create_logger_def(x),defs_l)
keys =      map(lambda x: create_logger_key(x),defs_l)
ifs =       map(lambda x: create_logger_if(x),defs_l)
decl =      map(lambda x: create_logger_decl(x),defs_l)

print 'Definitations for Logger.py:'
for i in logger:
	print i

print
print 'Keys for Logger.py:'
for i in keys:
	print i

print
print 'Declaretions for Logger.py:'
for i in decl:
	print i

print
print 'Ifs for Logger.py:'
for i in ifs:
	print i
	print

print
print 'Functions for log_protocol.h:'
for i in functions:
	print i
