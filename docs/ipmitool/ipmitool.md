CentOS release 6.2 (Final)
## 一、安装所需软件

### 1、查询下ipmi安装包
yum list |grep ipmi
ipmitool.x86_64 1.8.11-13.el6.1    @updates
ipmitool.x86_64 1.8.11-14.el6_4.1  update

### 2、安装ipmitool
yum -y install ipmitool

### 3、查看已安装的ipmi包
rpm -qa |grep ipmi
ipmitool-1.8.11-13.el6.1.x86_64

### 4、将ipmi服务添加到启动项
chkconfig ipmi on

### 5、5.1和5.2二选一查看

#### 5.1)、ls /etc/rc3.d/S13ipmi
lrwxrwxrwx 1 root root 14 May  6 16:26 /etc/rc3.d/S13ipmi -> ../init.d/ipmi

#### 5.2)、chkconfig --list|grep ipmi
ipmi 0:off    1:off    2:on    3:on    4:on    5:on    6:off

### 6、加载ipmi模块
modprobe ipmi_si && modprobe ipmi_devintf && modprobe ipmi_msghandler
### 7、查看模块
lsmod |grep ipmi
ipmi_si                42401  0 
ipmi_devintf            8049  0 
ipmi_msghandler        35992  2 ipmi_si,ipmi_devintf

### 8、启动ipmi
/etc/init.d/ipmi start
 
## 二、配置grub启动参数
cat /boot/grub/grub.conf|egrep -v "^#|^$"
default=0
timeout=5
title CentOS (2.6.32-220.el6.x86_64)
    root (hd0,0)
    kernel /boot/vmlinuz-2.6.32-220.el6.x86_64 ro root=/dev/sda1 selinux=0 console=tty0 console=ttyS1,115200 ro
    initrd /boot/initramfs-2.6.32-220.el6.x86_64.img
PS：添加console=tty0 console=ttyS1,115200在这个配置文件里
console=tty0 console=ttyS1,115200参数传递到内核中，实现串口重定向
console=tty0 代表显示器输出  
console=ttyS0 代表定向到串口1 ,如果是ttyS1代表定向到串口2
115200则为串口通信采用的波特率，波特率和bios设置的一样
 
## 三、通过ipmitool命令还可以对ipmi进行配置
1、查看ipmi信息
ipmitool lan print 1
2、设置BMC ip，作为远程管理ip
ipmitool lan set 1 ipaddr 172.16.*.*
3、连接目标终端
ipmitool -I lanplus -H 172.16.1. -U root -P 123456 sol activate
4、结束目标终端
ipmitool -I lanplus -H 172.16.1. -U root -P 123456 sol deactivate
5、重启目标终端
ipmitool -Ilanplus -H 172.16.1. -U root -P 123456 power reset
6、查看电源情况
ipmitool -I lanplus -H 172.16.1. -U root -P 123456 power status
7、开机
ipmitool -I lanplus -H 172.16.1. -U root -P 123456 power on
8、关机
ipmitool -I lanplus -H 172.16.1. -U root -P 123456 power off
9、修改bios启动项为网络启动
ipmitool -I lanplus -H 172.16.1. -U root -P 123456 chassis bootdev pxe
10、设置channel 1允许访问
ipmitool -I open lan set 1 access on
11、配置ipmi管理用户
ipmitool user set name 2 root
ipmitool user set password 2 "123456"
12、获取传感器中的各种监测值和该值的监测阈值，包括(CPU温度，电压，风扇转速，电源调制模块温度，电源电压等信息) 
ipmitool -I open sdr list(ipmitool -I open sensor)
13、显示温度
ipmitool sdr type Temperature
Temp             | 01h | ok  |  3.1 | -56 degrees C
Temp             | 02h | ok  |  3.2 | 50 degrees C
Temp             | 05h | ok  | 10.1 | 42 degrees C
Temp             | 06h | ns  | 10.2 | Disabled
Ambient Temp     | 0Eh | ok  |  7.1 | 20 degrees C
Planar Temp      | 0Fh | ok  |  7.1 | 37 degrees C
CPU Temp IF      | 76h | ns  |  7.1 | Disabled
Temp             | 0Ah | ok  |  8.1 | 31 degrees C
Temp             | 0Bh | ns  |  8.1 | Disabled
Temp             | 0Ch | unc |  8.1 | 45 degrees C
Ambient Temp     | 07h | ok  | 10.1 | 29 degrees C
Ambient Temp     | 08h | ns  | 10.2 | Disabled
当然也可以ipmitool sdr type直接回车
ipmitool sdr type
Sensor Types:
    Temperature                 Voltage                  
    Current                     Fan                      
    Physical Security           Platform Security        
    Processor                   Power Supply             
    Power Unit                  Cooling Device           
    Other                       Memory                   
    Drive Slot / Bay            POST Memory Resize       
    System Firmwares            Event Logging Disabled   
    Watchdog                    System Event             
    Critical Interrupt          Button                   
    Module / Board              Microcontroller          
    Add-in Card                 Chassis                  
    Chip Set                    Other FRU                
    Cable / Interconnect        Terminator               
    System Boot Initiated       Boot Error               
    OS Boot                     OS Critical Stop         
    Slot / Connector            System ACPI Power State  
    Watchdog                    Platform Alert           
    Entity Presence             Monitor ASIC             
    LAN                         Management Subsystem Health
    Battery                     Session Audit            
    Version Change              FRU State 
14、退出ipmi
shift ~ .
 
ipmitool命令参数说明
lan用于远程访问，电源管理等。 open用于本地访问。 lanplus用于sol。
 
三、inittab配置(因版本不同 配置有相应的变动)
cat /etc/inittab|egrep -v "^#|^$"
co:2345:respawn:/sbin/agetty ttyS1 115200 vt100-nav
设置ipmi必须需要注意 有的时候是ttyS1有的时候ttyS0  根据情况更改ttyS1还是ttyS0
/etc/inittab如何生效? 
生效的话需要执行init q(Q or q tell init to re-examine the /etc/inittab file. ) 
ps aux|grep tty
root      1137  0.0  0.0   4072   228 ttyS1    Ss+   2013   0:00 /sbin/agetty /dev/ttyS1 115200 vt100-nav
或执行start ttyS1