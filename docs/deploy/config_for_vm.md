#### 该虚拟机用于快速体验，下载后请参考以下信息修改配置

系统用户名：admin
密码： admin@123

1、 修改IP地址
```
# 根据实际情况，主要修改以下几处
[root@devops devops]# vi /etc/sysconfig/network-scripts/ifcfg-eno16777736
IPADDR=172.16.171.155
GATEWAY=172.16.171.2
NETMASK=255.255.255.0
DNS1=172.16.171.2

# 修改后保存退出并重启网络服务
systemctl restart network.service
```

2、配置dns静态解析
```
vi /etc/hosts
# 将IP地址修改为实际IP地址后保存
172.16.171.155 devops
```

3、配置salt-master接口
```
vi /etc/salt/master

将IP地址修改为实际IP地址后保存
interface: 172.16.171.155
```

4、配置salt-minion的master地址
```
vi /etc/salt/minion

将IP地址修改为实际 master IP地址后保存
master: 172.16.171.155
```

5、重启系统

6、登录应用

    http://ip:9000

    用户名：admin
    密码： admin@123

7、登录后配置服务

登录后在服务管理菜单将webssh和ftp服务的通信主机IP地址修改为虚拟机的IP地址


#### 默认已安装zabbix server(3.0)
zabbix server 默认不开启，如果需要zabbix，需修改相关配置并手动开启，参考如下步骤

1、启动zabbix-server
```
systemctl start zabbix-server
# 设置开机启动
systemctl enable zabbix-server
```

2、启动zabbix-server
```
# 修改配置文件
sed -i "s/Server=127.0.0.1/Server=server_ip/" /etc/zabbix/zabbix_agentd.conf
sed -i "s/ServerActive=127.0.0.1/ServerActive=server_ip/" /etc/zabbix/zabbix_agentd.conf
systemctl start zabbix-agent
# 设置开机启动
systemctl enable zabbix-agent

# 登录后要修改zabbix server主机的ip(127.0.0.1)地址为server_ip
```

3、登录zabbix web
    http://hostname_or_ip/zabbix

    用户名：Admin
    密码： zabbix


























