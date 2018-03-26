cd Firewall && make && ln -sf $PWD/fw.ko ../GUI/fw.ko
cd ../Syscall_Hooking_Manager && make && ln -sf $PWD/shm.ko ../GUI/shm.ko
cd ../Logger && ln -sf $PWD/Logger.py ../GUI/Logger.py

