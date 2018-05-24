Hey there! Welcome to the SecureMyTux project for defending your Linux from many networks attacks, spying on users in the system and get an information about what is happening in every second on your system.

This is our video that describes how the project works: https://www.youtube.com/watch?v=1cjJmoQH8QI

Must-Have:
	* A Linux system (Ubuntu should be good idea) with Kernel-Verision of 4+
	* Connection to the internet - for showing many attacks and defenses
	* package 'gcc' - sudo apt-get install gcc
	* python2 - sudo apt install python
	* package 'make' - sudo apt-get install make
	* python package 'tkinter' - sudo apt-get install python-tk
	* Python package ‘scapy’ - sudo pip install scapy

Mini-Guide:

	After you ensure that you have all the above packages, you should build the program by running the command `./SMT_build.sh` which builds SecureMyTux by your computer.
	If the builder tells you everything is OK, continue to the part of running the program - type `./SMT_run.sh` and the program should run.
	
	Next, enter admin's password in order to have permissions to run things such as kernel-module, read logs etc. In some cases you won't asked for password because the current screen has already saved it.

	Then, You have an 5 Options:
		* Turn On/Off the system
		* Show logs option - There you can show all logs (by empty textbox and `show all` select's option), delete all logs and search logs by a parameter as follows:
			By select one of the options in the select button and an empty text box - you will see all the options of the current select, for example, selecting `ip` option should show you all the ips that have been written in the logs.
			Then, if you want to get all the logs about specific option, you need to enter that instance of option (such as 192.168.1.1 when choosing `ip` option) in the textbox and press `show logs`.

		* Extra info - general information on the system, such as logged in users, get the sudoers group, show permissions of specific selected user, and show processes by specific selected user.
		
		* Feature Control - The configuration screen to enable components of the system, such as defenses of network attacks, and the blacklist screen, for blocking specific ip/mac.
		
		* Exit - exit the system, wait for the program to get closed.

Thanks very much!
We were Yan Poran and Nevo Biton with SecureMyTux
K33p Linux :)
	
