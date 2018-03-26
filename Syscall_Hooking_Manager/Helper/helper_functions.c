#include "helper_functions.h"


/* Gets a fd and returns the path it stands for
* Input: int fd - the fd to get his path
* Output: char* - the path as null terminated string
*/
char* get_path_by_fd(int fd)
{
    char *tmp = (char*)__get_free_page(GFP_TEMPORARY);

    struct file *file = fget(fd);
    if (!file) {
        goto out;
    }

    char *path = d_path(&file->f_path, tmp, PAGE_SIZE);
    if (IS_ERR(path)) {
        printk("error: %d\n", (int)path);
        goto out;
    }
out:
    free_page((unsigned long)tmp);

	return path;
}


/* Get a 2D array of strings and return a concatanation of them
* Input: char** argv - 2D strings array
* Output: char* - a concatanation of the 2D array strings
*/
char* matrix_strings_to_one_string(char* const argv[])
{
	char* all_argv;
	int i=0, size=0, last=0;

	while (argv[i])
	{
		size += strlen(argv[i]);
		i++;
	}
	last=i;
	size = size+(i*2)+(i-1)+1;  // i-1=',' ; 1=NULL ; i*2='""' ; size=length of the strings
	all_argv = (char*)kmalloc(size,GFP_KERNEL);
	all_argv[0] = NULL; //FOR strcat
	i=0;
	while (argv[i])
	{	
		strcat(all_argv,"\"");
		strcat(all_argv,argv[i]);
		i++;
		if(last == i)
		{
			strcat(all_argv,"\"\0"); //FOR strcat
		}
		else
		{
			strcat(all_argv,"\",\0"); //FOR strcat
		}
		
	}
	all_argv[size-1] = NULL;
	return all_argv;
}

