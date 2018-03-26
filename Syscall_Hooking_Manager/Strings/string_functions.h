#pragma once

#include <linux/kernel.h>
#include <linux/module.h>

#define MAX_WRITE 20
#define SIZE_WHITELIST 2
#define MAX_SIZE_DIR 20
#define TRUE 1
#define FALSE 0

size_t strlen(const char *s);
char *strstr(const char *s1, const char *s2);
char *strcat(char *dest, const char *src);
char *strcpy(char *dest, const char *src);