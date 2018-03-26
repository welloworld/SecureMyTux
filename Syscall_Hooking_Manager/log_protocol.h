#pragma once

#define MODULE_SIGNATURE "[SMT]"
#define ARP_PREFIX "[FA]"
#define DOS_PREFIX "[FD]"
#define RDHCP_PREFIX "[FR]"
#define FIREWALL_PREFIX "[FM]"
#define ERRORS_PREFIX "[FE]"
#define BLACKLIST_PREFIX "[FB]"
#define SYSCALL_HOOKING_MANAGER "[SH]"
#define SYSCALL_HOOKING_FILES "[SF]"
#define SYSCALL_HOOKING_SOCKETS "[SS]"
#define SYSCALL_HOOKING_DIRS "[SD]"
#define SYSCALL_HOOKING_PERMISSIONS "[SP]"
#define SYSCALL_HOOKING_FDS "[SC]" //OUT OF LETTES :(
#define SYSCALL_HOOKING_EXECUTIONS "[SE]"


#ifndef pr_fmt
#define pr_fmt(fmt) fmt

#endif

#define dmesg_error(fmt, ...) printk(KERN_EMERG MODULE_SIGNATURE ERRORS_PREFIX pr_fmt(fmt), ##__VA_ARGS__)
#define dmesg_firewall(fmt, ...) printk(KERN_INFO MODULE_SIGNATURE FIREWALL_PREFIX pr_fmt(fmt), ##__VA_ARGS__)
#define dmesg_dos(fmt, ...) printk(KERN_INFO MODULE_SIGNATURE DOS_PREFIX pr_fmt(fmt), ##__VA_ARGS__)
#define dmesg_blacklist(fmt, ...) printk(KERN_INFO MODULE_SIGNATURE BLACKLIST_PREFIX pr_fmt(fmt), ##__VA_ARGS__)    
#define dmesg_arp(fmt, ...) printk(KERN_INFO MODULE_SIGNATURE ARP_PREFIX pr_fmt(fmt), ##__VA_ARGS__)
#define dmesg_dhcp(fmt, ...) printk(KERN_INFO MODULE_SIGNATURE RDHCP_PREFIX pr_fmt(fmt), ##__VA_ARGS__)
#define dmesg_shm(fmt, ...) printk(KERN_INFO MODULE_SIGNATURE SYSCALL_HOOKING_MANAGER pr_fmt(fmt), ##__VA_ARGS__)
#define dmesg_shm_files(fmt, ...) printk(KERN_INFO MODULE_SIGNATURE SYSCALL_HOOKING_FILES pr_fmt(fmt), ##__VA_ARGS__)
#define dmesg_shm_sockets(fmt, ...) printk(KERN_INFO MODULE_SIGNATURE SYSCALL_HOOKING_SOCKETS pr_fmt(fmt), ##__VA_ARGS__)
#define dmesg_shm_dirs(fmt, ...) printk(KERN_INFO MODULE_SIGNATURE SYSCALL_HOOKING_DIRS pr_fmt(fmt), ##__VA_ARGS__)
#define dmesg_shm_permissions(fmt, ...) printk(KERN_INFO MODULE_SIGNATURE SYSCALL_HOOKING_PERMISSIONS pr_fmt(fmt), ##__VA_ARGS__)
#define dmesg_shm_fds(fmt, ...) printk(KERN_INFO MODULE_SIGNATURE SYSCALL_HOOKING_FDS pr_fmt(fmt), ##__VA_ARGS__)
#define dmesg_shm_executions(fmt, ...) printk(KERN_INFO MODULE_SIGNATURE SYSCALL_HOOKING_EXECUTIONS pr_fmt(fmt), ##__VA_ARGS__)