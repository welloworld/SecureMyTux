#include "sys_hook_manager.h"

void **sys_table;

//README deleted 

/* The init function for the module. Initializes the sys_table and all of the original syscalls we use.
* Hook all the syscalls we need with our own functions.
*/

int init_module(void)
{
	dmesg_shm("Syscall table is at: 0x%lx\n",address);
	
	sys_table = (void*)address;

	save_syscalls();
	change_syscalls();
	return 0;
}


/*
* The cleanup function for the module. Reverts the syscalls to the original ones (release the hooks)
*/
void cleanup_module(void)
{
	restore_syscalls();
	//dmesg_shm("Cleanup Made\n");
}

/* This function saves the current syscalls from the syscall table, to be called after the code execution is on our code.
*/
void save_syscalls(void) 
{
	//Save specific syscalls
	getuid_call = sys_table[__NR_getuid];
	getpid_call = sys_table[__NR_getpid];

	//Files:
	original_sys_read = sys_table[__NR_read];
	original_sys_write = sys_table[__NR_write];
	//original_sys_close = sys_table[__NR_close];
	original_sys_open = sys_table[__NR_open];
	original_sys_openat = sys_table[__NR_openat];
	original_sys_unlinkat = sys_table[__NR_unlinkat];
	original_sys_unlink = sys_table[__NR_unlink];

	//FDs:
	//original_sys_dup = sys_table[__NR_dup];
	//original_sys_dup2 = sys_table[__NR_dup2];
	//original_sys_pipe = sys_table[__NR_pipe];
	
	//Dirs:
	original_sys_rmdir = sys_table[__NR_rmdir];
	original_sys_mkdir = sys_table[__NR_mkdir];
	
	//Permissions:
	original_sys_chmod = sys_table[__NR_chmod];
	original_sys_fchmodat = sys_table[__NR_fchmodat];
	original_sys_fchmod = sys_table[__NR_fchmod];
	original_sys_chown = sys_table[__NR_chown];
	original_sys_fchown = sys_table[__NR_fchown];
	original_sys_lchown = sys_table[__NR_lchown];
	original_sys_fchownat = sys_table[__NR_fchownat];
	
	//Sockets:
	//original_sys_socket = sys_table[__NR_socket];
	original_sys_connect = sys_table[__NR_connect];
	//original_sys_listen = sys_table[__NR_listen];
	original_sys_bind = sys_table[__NR_bind];
	original_sys_accept = sys_table[__NR_accept];
	
	//Executions:
	original_sys_execve = sys_table[__NR_execve];
}
/* This function change the old syscalls (were saved) with our functions. 
*/
void change_syscalls(void) 
{
	write_cr0(read_cr0() & (~0x10000));   //For overwrite this section - we need to change the fifth bit from the right to 0 - the bit which responsible for the write protect 

	//sys_table[__NR_read] =     (void*)our_sys_read;     
	//sys_table[__NR_write] =    (void*)our_sys_write;    
	//sys_table[__NR_close] =    (void*)our_sys_close;    
	sys_table[__NR_open] =     (void*)our_sys_open;
	sys_table[__NR_openat] = (void*)our_sys_openat;     
	sys_table[__NR_unlinkat] = (void*)our_sys_unlinkat; 
	sys_table[__NR_unlink] =   (void*)our_sys_unlink;   
//
	//sys_table[__NR_dup] =      (void*)our_sys_dup;	  
	//sys_table[__NR_dup2] =     (void*)our_sys_dup2;    // Creates the new terminal opening error 
	//sys_table[__NR_pipe] =     (void*)our_sys_pipe;    // Creates a problem when trying to 'tab' vim.. If you don't understand what I mean-ask Yan
	
	sys_table[__NR_rmdir] =    (void*)our_sys_rmdir;    
	sys_table[__NR_mkdir] =    (void*)our_sys_mkdir;    
	
	sys_table[__NR_chmod] =    (void*)our_sys_chmod;    
	sys_table[__NR_fchmodat] = (void*)our_sys_fchmodat; 
	sys_table[__NR_fchmod] =   (void*)our_sys_fchmod;   
	sys_table[__NR_chown] = (void*)our_sys_chown;
	sys_table[__NR_fchown] = (void*)our_sys_fchown;
	sys_table[__NR_lchown] = (void*)our_sys_lchown;
	sys_table[__NR_fchownat] = (void*)our_sys_fchownat;

	////sys_table[__NR_socket] = (void*)our_sys_socket;     //DO WE NEED THIS?
	sys_table[__NR_connect] = (void*)our_sys_connect;   
	////sys_table[__NR_listen] = (void*)our_sys_listen;     //DO WE NEED THIS?
	sys_table[__NR_bind] = (void*)our_sys_bind;         
	sys_table[__NR_accept] = (void*)our_sys_accept;     //2 - Accept only 0's (why?)

	sys_table[__NR_execve] = (void*)our_sys_execve;

	write_cr0(read_cr0() | 0x10000); //Return to the same bits before the write change 
}
/* This function restores the original syscalls to the syscalls we have changed. 
*/
void restore_syscalls(void) 
{
	write_cr0(read_cr0() & (~0x10000)); //For overwrite this section - we need to change the fifth bit from the right to 0 - the bit which responsible for the write protect 

	//sys_table[__NR_read] = (void*)original_sys_read;
	//sys_table[__NR_write] = (void*)original_sys_write;
//	sys_table[__NR_close] = (void*)original_sys_close;
	sys_table[__NR_open] = (void*)original_sys_open;
	sys_table[__NR_openat] = (void*)original_sys_openat;
	sys_table[__NR_unlinkat] = (void*)original_sys_unlinkat;
	sys_table[__NR_unlink] = (void*)original_sys_unlink;

	//sys_table[__NR_dup] = (void*)original_sys_dup;
	//sys_table[__NR_dup2] = (void*)original_sys_dup2;
	//sys_table[__NR_pipe] = (void*)original_sys_pipe;
	
	sys_table[__NR_rmdir] = (void*)original_sys_rmdir;
	sys_table[__NR_mkdir] = (void*)original_sys_mkdir;

	sys_table[__NR_chmod] = (void*)original_sys_chmod;
	sys_table[__NR_fchmodat] = (void*)original_sys_fchmodat;
	sys_table[__NR_fchmod] = (void*)original_sys_fchmod;
	sys_table[__NR_chown] = (void*)original_sys_chown;
	sys_table[__NR_fchown] = (void*)original_sys_fchown;
	sys_table[__NR_lchown] = (void*)original_sys_lchown;
	sys_table[__NR_fchownat] = (void*)original_sys_fchownat;

	////sys_table[__NR_socket] = (void*)original_sys_socket;
	sys_table[__NR_connect] = (void*)original_sys_connect;
	////sys_table[__NR_listen] = (void*)original_sys_listen;
	sys_table[__NR_bind] = (void*)original_sys_bind;
	sys_table[__NR_accept] = (void*)original_sys_accept;

	sys_table[__NR_execve] = (void*)original_sys_execve;

	write_cr0(read_cr0() | 0x10000); //Return to the same bits before the write change 
}
/*#############################                        Files:                          ############################### */

/* Hook function for the read syscall, prints the file path, user id, pid, and buffer, than calls original sys_read
*/
asmlinkage ssize_t our_sys_read(int fd,void *buf,size_t count)
{
	const char* path = get_path_by_fd(fd);
	if(is_readable_and_not_from_project(buf) && !in_blacklist(path) && !strstr(buf, "\\xdf\\xdf\\xdf\\xdf"))
	{
		dmesg_shm_files("Read: path=%s | uid=%d | pid=%d | buf=%s\n",path, getuid_call(),getpid_call(),(char*)buf);
		
	}
	return original_sys_read(fd, buf, count);
}

/* This function is our extension for the write syscall, it filters and prints the data (if it readable).
*/
asmlinkage ssize_t our_sys_write(int fd,const char *buf,size_t count)
{
	//Path does not work

	if(is_readable_and_not_from_project(buf))
	{
		dmesg_shm_files("Write: fd=%d | pid=%d | buf=%s | count=%zd\n",fd, getpid_call(),buf,count);
	}

	return original_sys_write(fd, buf, count);
}

/* This function is our extension for the close syscall. It prints the fd who called the close.
*/
asmlinkage int our_sys_close(int fd)
{
	dmesg_shm_files("Close: fd=%d\n",fd); 
	return original_sys_close(fd);
}

/* Hook function for the open syscall, prints the filename, user id, pid, flag and mode, than calls original sys_open
*/
asmlinkage int our_sys_open(const char *path,int flags,mode_t mode)
{
	
	if(filter_dir_or_files(path))
	{
		dmesg_shm_files("Open: path=%s | uid=%d | pid=%d\n",path,getuid_call(), getpid_call());
	}

	return original_sys_open(path, flags, mode);
}

/* Hook function for the openat syscall, prints the filename, user id, pid, and flag, than calls original sys_openat
*/
asmlinkage int our_sys_openat(int dfd,const char *path,int flag,mode_t mode)
{
	if(filter_dir_or_files(path))
	{
		if(dfd < 0)
		{
			dmesg_shm_files("Openat: path=%s | uid=%d | pid=%d\n",path,getuid_call(),getpid_call());
		}
		else
		{
			//WE DONT WANT TO SEE IT
			//dmesg_shm_files("Openat: fd=%d | flag=%d | User=%d | Mode=%d\n",dfd,flag,getuid_call(),mode&0777); //every syscall with dfd that < 0 would print here - has no filename so it cant be in the blacklist
		}
	}
	return original_sys_openat(dfd, path, flag, mode);
}

/* Hook function for the unlinkat syscall, prints the file path, flag, and user id, than calls original sys_unlinkat
*/
asmlinkage int our_sys_unlinkat(int dfd,const char * pathname,int flag)
{
	if(filter_dir_or_files(pathname))
	{
		if(dfd < 0)
		{
			dmesg_shm_files("Unlinkat: path=%s | uid=%d\n",pathname,getuid_call());
		}
		else
		{
			char* path = get_path_by_fd(dfd);
			dmesg_shm_files("Unlinkat: path=%s | uid=%d\n",path,getuid_call()); 
		}
		
	}
	return original_sys_unlinkat(dfd, pathname, flag);
}

/* Hook function for the unlink syscall, prints the file path and user id, than calls original sys_unlink
*/
asmlinkage int our_sys_unlink(const char *pathname)
{
	if(filter_dir_or_files(pathname))
	{
		dmesg_shm_files("Unlink: path=%s | uid=%d\n",pathname,getuid_call());
	}
	return original_sys_unlink(pathname);
}


/*#############################                        FDs:                          ############################### */

/* Hook function for the dup syscall, prints the old fd, new fd, and path, than calls original sys_dup
*/
asmlinkage int our_sys_dup(int fd)
{
	//char* path = get_path_by_fd(fd); //We don't use this syscall anymore!
	//dmesg_shm_fds("Dup: old fd=%d | path: %s\n",fd,path);
	return original_sys_dup(fd);
}

/* Hook function for the dup2 syscall, prints the old fd, new fd, and path, than calls original sys_dup2
*/
asmlinkage int our_sys_dup2(int oldfd,int newfd)
{
	if(oldfd > -1 && newfd > -1)
	{
		//char* path = get_path_by_fd(oldfd); //Causes terminal opening problems
		//dmesg_shm_fds("Dup2: old fd=%d | new fd=%d \n",oldfd,newfd); //We don't use this syscall anymore!
	}
	
	return original_sys_dup2(oldfd,newfd);
}

/* Hook function for the pipe syscall, prints the read fd, write  fd, and path for both, than calls original sys_pipe
*/
asmlinkage int our_sys_pipe(int *fildes)
{
	if (fildes[0] != -1 && fildes[1] != -1)
	{
		//char* rpath = get_path_by_fd(fildes[0]);
		//char* wpath = get_path_by_fd(fildes[1]); //We don't use this syscall anymore!
		//dmesg_shm_fds("Pipe: Read_fd=%d path=%s | Write_fd=%d path=%s\n",fildes[0], rpath,fildes[1], wpath);
	}
	return original_sys_pipe(fildes);
}

/*#############################                        Dirs:                          ############################### */

/* Hook function for the rmdir syscall, prints the path and user id, than calls original sys_rmdir
*/
asmlinkage int our_sys_rmdir(const char *pathname)
{
	if(filter_dir_or_files(pathname))
	{
		dmesg_shm_dirs("Rmdir: path=%s | uid=%d\n",pathname,getuid_call());
	}
	return original_sys_rmdir(pathname);
}

/* Hook function for the mkdir syscall, prints the path, mode and user id, than calls original sys_mkdir
*/
asmlinkage int our_sys_mkdir(const char *pathname,mode_t mode)
{
	if(filter_dir_or_files(pathname))
	{
		dmesg_shm_dirs("Mkdir: path=%s | mode=%3o | uid=%d\n",pathname,mode&0777,getuid_call());
	}
	return original_sys_mkdir(pathname, mode);
}

/*#############################                        Permissions:                          ############################### */

/* Hook function for the chmod syscall, prints the path, mode and user id, than calls original sys_chmod
*/
asmlinkage int our_sys_chmod(const char *path,mode_t mode)
{
	dmesg_shm_permissions("Chmod: path=%s | mode=%3o | uid=%d\n",path,mode&0777,getuid_call());
	return original_sys_chmod(path, mode);
}

/* Hook function for the fchmodat syscall, prints the path, mode and user id, than calls original sys_fchmodat
*/
asmlinkage int our_sys_fchmodat(int dfd,const char * path,mode_t mode)
{
	char* patht;
	if(dfd < 0)
	{
		dmesg_shm_permissions("Fchmodat: path=%s | mode=%3o | uid=%d\n",path,mode&0777,getuid_call());
	}
	else
	{
		patht = get_path_by_fd(dfd);
		dmesg_shm_permissions("Fchmodat: path=%s | mode=%3o | uid=%d\n",patht,mode&0777,getuid_call());
	}
	return original_sys_fchmodat(dfd, path, mode);
}

/* Hook function for the fchmod syscall, prints the path, mode and user id, than calls original sys_fchmod
*/
asmlinkage int our_sys_fchmod(int fd,mode_t mode)
{
	char* path = get_path_by_fd(fd);
	dmesg_shm_permissions("Fchmod: path=%s | mode=%3o | uid=%d\n",path,mode&0777,getuid_call());
	return original_sys_fchmod(fd, mode);
}

/* Hook function for the chown syscall, prints the path, user id and group id, than calls original sys_chown
*/
asmlinkage int our_sys_chown(const char *path,int user,int group)
{
	dmesg_shm_permissions("Chown: path=%s | user=%d | group=%d\n",path,user,group);
	return original_sys_chown(path, user, group);
}

/* Hook function for the fchown syscall, prints the path, user id and group id, than calls original sys_fchown
*/
asmlinkage int our_sys_fchown(int fd,int user,int group)
{
	char* path = get_path_by_fd(fd);
	dmesg_shm_permissions("Fchown: path=%s | user=%d | group=%d\n",path,user,group);
	return original_sys_fchown(fd, user, group);
}

/* Hook function for the chown syscall, prints the path, user id, group id and flag, than calls original sys_chown
*/
asmlinkage int our_sys_fchownat(int dfd,const char *patht,int user,int group,int flag)
{
	char * path;
	if(dfd < 0)
	{
		dmesg_shm_permissions("Fchownat: path=%s | user=%d | group=%d\n",patht,user,group);
	}
	else
	{
		path = get_path_by_fd(dfd);
		dmesg_shm_permissions("Fchownat: path=%s | user=%d | group=%d\n",path,user,group);
	}
	return original_sys_fchownat(dfd, patht, user, group, flag);
}

/* Hook function for the lchown syscall, prints the filename, user id and group id, than calls original sys_lchown
*/
asmlinkage int our_sys_lchown(const char *path,int user,int group)
{
	dmesg_shm_permissions("Chown: path=%s | user=%d | group=%d\n",path,user,group);
	return original_sys_lchown(path, user, group);
}


/*#############################                        Sockets:                          ############################### */

/* Hook function for the connect syscall, prints the sockfd, family, port and address, than calls original sys_connect
*/
asmlinkage int our_sys_connect(int sockfd,const struct sockaddr_in *addr,int addrlen)
{
	unsigned char* ip = (unsigned char*)&addr->sin_addr.s_addr;
	dmesg_shm_sockets("Connect: sockfd=%d | family=%d | port=%hu | ip=%d.%d.%d.%d\n",sockfd,addr->sin_family,htons(addr->sin_port),ip[0],ip[1],ip[2],ip[3]);
	return original_sys_connect(sockfd, addr, addrlen);
}

/* Hook function for the bind syscall, prints the sockfd, family, port and address, than calls original sys_bind
*/
asmlinkage int our_sys_bind(int sockfd, const struct sockaddr_in *addr,int addrlen)
{
	unsigned char* ip = (unsigned char*)&addr->sin_addr.s_addr;
	dmesg_shm_sockets("Bind: sockfd=%d | family=%d | port=%hu | ip=%d.%d.%d.%d\n",sockfd,addr->sin_family,htons(addr->sin_port),ip[0],ip[1],ip[2],ip[3]);
	return original_sys_bind(sockfd, addr, addrlen);
}

/* Hook function for the accept syscall, prints the sockfd, family, port and address, than calls original sys_accept
*/
asmlinkage int our_sys_accept(int sockfd,const struct sockaddr_in *addr, int *addrlen)
{
	if(addrlen && addr)
	{
		unsigned char* ip = (unsigned char*)&addr->sin_addr.s_addr;
		dmesg_shm_sockets("Accept: sockfd=%d | family=%d | port=%hu | ip=%d.%d.%d.%d\n",sockfd,addr->sin_family,htons(addr->sin_port),ip[0],ip[1],ip[2],ip[3]);
	}
	return original_sys_accept(sockfd, addr, addrlen);
}
/*
asmlinkage int our_sys_socket(int domain, int type, int protocol)
{
	dmesg_shm("s Called:\n"); //DO WE NEED THAT FUNCTION ?
	return original_sys_socket(domain, type, protocol);
}

asmlinkage int our_sys_listen(int sockfd, int backlog)
{
	dmesg_shm("sys_listen Called\n");
	return original_sys_listen(sockfd, backlog);
}*/


/*#############################                        Executions:                          ############################### */

/* Hook function for the execve syscall, prints the filename, argv, user id and pid, than calls original sys_execve
*/
asmlinkage int our_sys_execve(const char *path, char *const argv[],char *const envp[])
{
	char *args = matrix_strings_to_one_string(argv);
	//char *envs = matrix_strings_to_one_string(envp); // A lots of shit
	if (filter_execve(path,args))
	{
		dmesg_shm_executions("Execve: path=%s | argv=[%s] | uid=%d | pid=%d\n",path,args,getuid_call(),getpid_call()); 
	}
	kfree(args);
	
	return original_sys_execve(path, argv, envp);
}

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Here to secure you");
MODULE_AUTHOR("Yan Poran & Nevo Biton");
