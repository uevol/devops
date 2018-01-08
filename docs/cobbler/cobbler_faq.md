# FAQ about cobbler
### xmlrpclib.Fault: <Fault 1: "<class 'cobbler.cexceptions.CX'>:'login failed'">
解决方法：
```
service cobblerd restart
cobbler get-loaders
```

### apr_sockaddr_info_get() failed for cobbler
解决方法：
```
vi /etc/hosts
cobbler_ip fqdn hostname
```

### PXE-E32:TFTP open timeout TFTP"Open"
查找PXE启动芯片出错代码表，是说tftp没有运行,请求没有应答
解决方法：验证TFTP服务是否正在运行
```
service xinetd restart
netstat -nlatup | grep 69

udp        0      0 0.0.0.0:69                  0.0.0.0:*                               6621/xinetd
```

### Cobbler 安装状态获取 ###
通过cobbler status命令可以获取安装进度
```
[root@cobbler ~]# cobbler status
ip             |target              |start            |state            
192.168.3.125  |system:linux        |Fri Jun 30 11:31:29 2017|unknown/stalled  
192.168.3.151  |system:test         |Mon Jul  3 11:13:05 2017|finished         
192.168.3.154  |system:test         |Mon Jul  3 11:26:47 2017|installing (0m 16s)
192.168.3.39   |system:xyz          |Tue Jun 27 15:46:36 2017|finished         
[root@cobbler ~]# cobbler status
ip             |target              |start            |state            
192.168.3.125  |system:linux        |Fri Jun 30 11:31:29 2017|unknown/stalled  
192.168.3.151  |system:test         |Mon Jul  3 11:13:05 2017|finished         
192.168.3.154  |system:test         |Mon Jul  3 11:26:47 2017|finished         
192.168.3.39   |system:xyz          |Tue Jun 27 15:46:36 2017|finished   
```

也可以通过查看/var/log/cobbler/install.log获取

> https://github.com/cobbler/cobbler/issues/1261


### default启动配置 ####
```
修改 /var/lib/tftpboot/pxelinux.cfg
ONTIMEOUT LiveV3  <local 改为 LiveV3>

LABEL LiveV3
        kernel /images/LiveV3/vmlinuz0
        MENU LABEL LiveV3
        MENU DEFAULT   <添加这一行，原先的local里面把这行去掉>
        append initrd=/images/LiveV3/initrd0.img ksdevice=bootif installserverip=192.168.3.166 text rd.dm=0 vga=791 nolvmmount liveimg rootfstype=auto lang=  kssendmac quiet rd.md=0 rhgb 3 rd.luks=0 ro root=live:/LiveV3.iso  ks=http://192.168.3.166/cblr/svc/op/ks/profile/LiveV3
        ipappend 2

```

### 固定重eth0启动当服务器有多个网卡 ####
```
vi /etc/sysconfig/dhcpd 
# Command line options here
DHCPDARGS=eth0
```

