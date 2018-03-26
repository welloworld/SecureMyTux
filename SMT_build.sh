cd Firewall && make
cp fw.ko ../GUI/fw.ko
cd ../Syscall_Hooking_Manager && make
cp shm.ko ../GUI/shm.ko
