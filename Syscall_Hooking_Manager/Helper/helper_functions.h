#pragma once

#include <linux/kernel.h>
#include <linux/module.h>
#include <asm/unistd.h>
#include <asm/cacheflush.h>
#include <linux/slab.h>//for kmalloc and kfree
#include <linux/socket.h>
#include <linux/in.h>
#include <linux/file.h>//needed?
//#include <linux/lockdep.h>//needed? - for using task_struct
#include <linux/fdtable.h>
#include <linux/fs.h>
#include <linux/unistd.h>
#include <asm/syscall.h>
#include "../Strings/string_functions.h"

#define MAX_WRITE 20
#define SIZE_WHITELIST 2
#define MAX_SIZE_DIR 20
#define TRUE 1
#define FALSE 0

char * get_path_by_fd(int fd);
char* matrix_strings_to_one_string(char* const argv[]);

