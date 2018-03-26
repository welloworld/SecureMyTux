#include "filters.h"


// holds an array of directory paths that the user want them to be tracked
char* dirs_whitelist[MAX_SIZE_DIR] = {
	"/home\0","/wello\0"
}; 


// holds an array of directory paths that the user don't want them to be tracked
//Add bin to bl
char* files_blacklist[MAX_SIZE_BL] = {
	"conf\0","setting\0","chrome\0","/dev/kmsg\0"
}; 


/* Check if a string should be filtered or not. Returns TRUE(1) if should be filtered and FALSE (0) otherwise
* Input: a null terminated string,
		 an int which flags filter project made output (Passing TRUE = filter, passing FALSE = ignore examination)
* Output: Return TRUE (1) if the string length is between 4 to 50 and is composed of readable ascii only (also \n \t \0),
		  otherwise FALSE (0). If project made output filter is flagged on it will also check if the string contains "SMT" to return TRUE (1) 
*/
int is_readable_and_not_from_project(char buf[]) //**/
{
	
	int i=0;
	int count = strlen(buf);
	if (count < 4 /*|| count > 50*/)
	{
		return FALSE;
	}
	for(i=0;i<count;i++)
	{
		if(!(buf[i] <= '~' && buf[i] >= ' ') && (buf[i] != '\n' || buf[i] != '\t' || buf[i] != '\0')) //Readable Ascii
		{
			return FALSE; //Not to be printed
		}
	}
	buf[i]=NULL;
	if(strstr(buf,"SMT"))
	{
		return FALSE; //Not to be printed
	}
	return TRUE;
}


/* Returns TRUE if execve args contain blacklisted strings, otherwise FALSE
* Input: string s1 - filename sent to execve, string s2 - args sent to execve after concat' to one string
* Output: int - TRUE if args blacklisted, FALSE otherwise
*/
int filter_execve(const char * s1,const char* s2)
{
	if (in_blacklist(s1) || in_blacklist(s2))
	{
		return FALSE;
	}
	return TRUE;
}


/* Multi-purpose path filter, returns if should filter (TRUE) or FALSE if shouldn't.
* Input: int whitelist - Gets TRUE if you want to check for the path in the whitelist, FALSE otherwise
		 int reg_files - Gets TRUE if you want to check if the path is a filename, FALSE otherwise
		 null terminated string path - the path in question
		 int config - Gets TRUE if you want to check that the path doesnt contain "config", FALSE otherwise
* Output: Returns FALSE by default, if the path is 1 char long and is "." or "/" return TRUE
		  the rest depends on the parameters as mentioned in 'Input'
*/
int filter_dir_or_files(const char* path)
{
	//if((in_whitelist(filename) || filename[0] != '/') && (!(strstr(filename,"config"))))
	int flag=0;
	if(in_whitelist(path) || path[0] != '/')
	{
		flag=1;
	}
	if(strstr(path,"config"))
	{
		flag=0;
	}
	if(strlen(path) == 1 && (strstr(path,".") || strstr(path,"/")))
	{
		flag=0;
	}
	return flag;
}


/* Check if a string in li is contained in path, 
*  if one does than return TRUE, otherwise return FALSE
* Input: char** li - list of strings to search in path
		 char* path - the path to search in
		 int size - the amount of string in li (2D array size)
* Output: TRUE if a match is found, FALSE otherwise
*/
int search_in_list_of_strings(char** li,const char* path, int size)
{
	int i=0;
	//**/Removed old code
	for (i=0;i < size; i++)
	{
		if (strstr(path,li[i]))
		{
			return 1;
		}
	}
	return 0;
}


/* Checks if a path is in whitelist
* Input: char* path - the path to check
* Output: returns TRUE if in whitelist, FALSE otherwise
*/
int in_whitelist(const char* path)
{
	return search_in_list_of_strings(dirs_whitelist,path,SIZE_WHITELIST);
}


/* Checks if a path is in blacklist
* Input: char* path - the path to check
* Output: returns TRUE if in blacklist, FALSE otherwise
*/
int in_blacklist(const char* path)
{
	return search_in_list_of_strings(files_blacklist,path,SIZE_BLACKLIST);
}

