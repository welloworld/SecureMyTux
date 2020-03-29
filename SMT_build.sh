sudo apt-get install make gcc python2.7 scapy python-tk
cd Firewall && make clean > /dev/null 2>&1 && make > /dev/null 2>&1 && ln -sf $PWD/fw.ko ../GUI/fw.ko
cd ../Syscall_Hooking_Manager && make clean > /dev/null 2>&1 && make > /dev/null 2>&1 && ln -sf $PWD/shm.ko ../GUI/shm.ko
cd ../Logger && ln -sf $PWD/Logger.py ../GUI/Logger.py
cd ..
if [ -f Syscall_Hooking_Manager/shm.ko ] && [ -f Firewall/fw.ko ]; then
	echo "Everything is Good!"
else
	echo "You have some problems.."	
fi

