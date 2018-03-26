#pragma once
#include <linux/kernel.h>
#include <linux/module.h>
#include <asm/unistd.h>
#include <asm/cacheflush.h>
#include <linux/slab.h>
#include <linux/socket.h>
#include <linux/in.h>
#include <linux/file.h>
//**/

#include <linux/unistd.h>
#include <asm/syscall.h>

#include "log_protocol.h"
#include "Strings/string_functions.h"
#include "Filters/filters.h"
#include "Helper/helper_functions.h"


#define MAX_WRITE 20
#define SIZE_WHITELIST 2
#define MAX_SIZE_DIR 20
#define TRUE 1
#define FALSE 0

int init_module(void);
void cleanup_module(void);	

void change_syscalls(void);
void save_syscalls(void);
void restore_syscalls(void);


asmlinkage ssize_t (*original_sys_read) (int fd,void *buf,size_t count);
asmlinkage ssize_t our_sys_read(int fd,void *buf,size_t count);

asmlinkage ssize_t (*original_sys_write) (int fd,const char *buf,size_t count);
asmlinkage ssize_t our_sys_write(int fd,const char *buf,size_t count);

asmlinkage int (*original_sys_close) (int fd);
asmlinkage int our_sys_close(int fd);

asmlinkage int (*original_sys_dup) (int fildes);
asmlinkage int our_sys_dup(int fd);

asmlinkage int (*original_sys_dup2) (int oldfd,int newfd);
asmlinkage int our_sys_dup2(int oldfd,int newfd);

asmlinkage int (*original_sys_pipe) (int *fildes);
asmlinkage int our_sys_pipe(int *fildes);

asmlinkage int (*original_sys_rmdir) (const char *pathname);
asmlinkage int our_sys_rmdir(const char *pathname);

asmlinkage int (*original_sys_mkdir) (const char *pathname,mode_t mode);
asmlinkage int our_sys_mkdir(const char *pathname,mode_t mode);

asmlinkage int (*original_sys_chmod) (const char *filename,mode_t mode);
asmlinkage int our_sys_chmod(const char *filename,mode_t mode);

asmlinkage int (*original_sys_fchmodat) (int dfd,const char * filename,mode_t mode);
asmlinkage int our_sys_fchmodat(int dfd,const char * filename,mode_t mode);

asmlinkage int (*original_sys_fchmod) (int fd,mode_t mode);
asmlinkage int our_sys_fchmod(int fd,mode_t mode);

asmlinkage int (*original_sys_unlinkat) (int dfd,const char * pathname,int flag);
asmlinkage int our_sys_unlinkat(int dfd,const char * pathname,int flag);

asmlinkage int (*original_sys_unlink) (const char *pathname);
asmlinkage int our_sys_unlink(const char *pathname);

asmlinkage int (*original_sys_open) (const char *filename,int flags,mode_t mode);
asmlinkage int our_sys_open(const char *filename,int flags,mode_t mode);

asmlinkage int (*original_sys_connect) (int sockfd,const struct sockaddr_in *addr,int addrlen);
asmlinkage int our_sys_connect(int sockfd,const struct sockaddr_in *addr,int addrlen);

asmlinkage int (*original_sys_bind) (int sockfd, const struct sockaddr_in *addr,int addrlen);
asmlinkage int our_sys_bind(int sockfd, const struct sockaddr_in *addr,int addrlen);

asmlinkage int (*original_sys_accept) (int sockfd,const struct sockaddr_in *addr, int *addrlen);
asmlinkage int our_sys_accept(int sockfd,const struct sockaddr_in *addr, int *addrlen);

asmlinkage int (*getuid_call)(void);
asmlinkage int (*getpid_call)(void);
/*
asmlinkage int (*original_sys_socket) (int domain, int type, int protocol);
asmlinkage int our_sys_socket(int domain, int type, int protocol);

asmlinkage int (*original_sys_listen) (int sockfd, int backlog);
asmlinkage int our_sys_listen(int sockfd, int backlog);
*/

asmlinkage int (*original_sys_execve) (const char *filename, char *const argv[],char *const envp[]);
asmlinkage int our_sys_execve(const char *filename, char *const argv[],char *const envp[]);

asmlinkage int (*original_sys_chown) (const char *filename,int user,int group);
asmlinkage int our_sys_chown(const char *filename,int user,int group);

asmlinkage int (*original_sys_fchown) (int fd,int user,int group);
asmlinkage int our_sys_fchown(int fd,int user,int group);

asmlinkage int (*original_sys_lchown) (const char *filename,int user,int group);
asmlinkage int our_sys_lchown(const char *filename,int user,int group);

asmlinkage int (*original_sys_fchownat) (int dfd,const char *filename,int user,int group,int flag);
asmlinkage int our_sys_fchownat(int dfd,const char *filename,int user,int group,int flag);

asmlinkage int (*original_sys_openat) (int dfd,const char *filename,int flags,mode_t mode);
asmlinkage int our_sys_openat(int dfd,const char *filename,int flags,mode_t mode);

//*

//Get the address parameter with the right permissions
static unsigned long address = 0;
module_param(address, ulong, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH); 
