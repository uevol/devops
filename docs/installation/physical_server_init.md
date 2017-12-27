物理机初始化过程
1.配置IPMI
	- 主机启动后，进入BIOS，设置IPMI地址、用户名、密码(192.168.3.200  Administrator R00t@123)

2.添加LiveCD   <cobbler-server:192.168.3.166 root R00t@123 >
    - #cobbler distro add --name=CentOS-6.8-x86_64-LiveCD --kernel=/srv/livecd/vmlinuz0 --initrd=/srv/livecd/initrd0.img
    - # cobbler distro edit --name=CentOS-6.8-x86_64-LiveCD --kopts='rootfstype=auto installserverip=@@http_server@@ rd.dm=0 quiet rd.md=0 vga=791 rhgb 3 rd.luks=0 nolvmmount liveimg ro root=live:/CentOS-6.8-x86_64-LiveCD.iso' 
    - #cobbler profile add --name=CentOS-6.8-x86_64-LiveCD --distro=CentOS-6.8-x86_64-LiveCD

3.cobbler添加system
	- #cobbler system add --name=xyz --mac=AA:BB:CC:DD:EE:FF --profile=CentOS-6.8-x86_64-LiveCD  --interface=eth0	

2.IPMI启动物理机
	- #ipmitool -H 192.168.3.200 -U Administrator  -P R00t@123 -I lanplus chassis bootdev pxe
	- #ipmitool -H 192.168.3.200 -U Administrator  -P R00t@123 -I lanplus chassis power on

3.megacli怎么样把raid的配置传进去？参照
http://jaseywang.me/2013/05/18/使用-dtk-自动批量建立-raid/	
http://blog.csdn.net/lizhihua0925/article/details/53198483