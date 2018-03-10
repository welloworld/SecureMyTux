sudo insmod shm.ko address=0x$(sudo cat /proc/kallsyms | grep sys_call_table | head -1 | cut -f 1 -d" ")
