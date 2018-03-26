#pragma once

#include <linux/kernel.h>
#include <linux/module.h>

#define MAX_WRITE 20

#define SIZE_WHITELIST 2
#define MAX_SIZE_DIR 20

#define MAX_SIZE_BL 20
#define SIZE_BLACKLIST 4

#define TRUE 1
#define FALSE 0

int in_whitelist(const char* path);
int in_blacklist(const char* path);
int is_readable_and_not_from_project(char buf[]); /*int filter_data(char buf[],int no_project);*/ //*
int filter_dir_or_files(const char* path);
int filter_execve(const char * s1,const char* s2);
int search_in_list_of_strings(char** li,const char* path, int size);

