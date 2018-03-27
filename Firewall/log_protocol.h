#pragma once

#define MODULE_SIGNATURE "[SMT]"
#define ARP_PREFIX "[FA]"
#define DOS_PREFIX "[FD]"
#define RDHCP_PREFIX "[FR]"
#define FIREWALL_PREFIX "[FM]"
#define ERRORS_PREFIX "[FE]"
#define BLACKLIST_PREFIX "[FB]"

#ifndef pr_fmt
#define pr_fmt(fmt) fmt

#endif

#define dmesg_error(fmt, ...) printk(KERN_EMERG MODULE_SIGNATURE ERRORS_PREFIX pr_fmt(fmt), ##__VA_ARGS__)

#define dmesg_firewall(fmt, ...) printk(KERN_INFO MODULE_SIGNATURE FIREWALL_PREFIX pr_fmt(fmt), ##__VA_ARGS__)

#define dmesg_dos(fmt, ...) printk(KERN_INFO MODULE_SIGNATURE DOS_PREFIX pr_fmt(fmt), ##__VA_ARGS__)

#define dmesg_blacklist(fmt, ...) printk(KERN_INFO MODULE_SIGNATURE BLACKLIST_PREFIX pr_fmt(fmt), ##__VA_ARGS__)    

#define dmesg_arp(fmt, ...) printk(KERN_INFO MODULE_SIGNATURE ARP_PREFIX pr_fmt(fmt), ##__VA_ARGS__)

#define dmesg_dhcp(fmt, ...) printk(KERN_INFO MODULE_SIGNATURE RDHCP_PREFIX pr_fmt(fmt), ##__VA_ARGS__)    