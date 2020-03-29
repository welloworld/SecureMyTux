# SecureMyTux #

Welcome to the `SecureMyTux` project for defending your Linux from many networks attacks, spying on users in the system and get an information about what is happening in every second on your system.


This is our video that describes how the project works: https://www.youtube.com/watch?v=1cjJmoQH8QI

## Build & Run ##
1. `./SMT_build.sh`
2. `./SMT_run.sh`, and enter password (for inserting a kernel module).

## System managment ##
Then, You have a screen with 5 Options:
* Turn On/Off the system
* Show logs option - There you can show all logs (by empty textbox and `show all` select's option), delete all logs and search logs by a parameter as follows:
	By select one of the options in the select button and an empty text box - you will see all the options of the current select, for example, selecting `ip` option should show you all the ips that have been written in the logs.
	Then, if you want to get all the logs about specific option, you need to enter that instance of option (such as 192.168.1.1 when choosing `ip` option) in the textbox and press `show logs`.
* Extra info - general information on the system, such as logged in users, get the sudoers group, show permissions of specific selected user, and show processes by specific selected user.
* Feature Control - The configuration screen to enable components of the system, such as defenses of network attacks, and the blacklist screen, for blocking specific ip/mac.
* Exit - exit the system, wait for the program to get closed.

We were Yan Poran and Nevo Biton with SecureMyTux

K33p Linux :)
