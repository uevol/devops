yu# important 
相关软件版本：
salt-minion-2016.11.6-1.el6.noarch
salt-2016.11.6-1.el6.noarch
salt-api-2016.11.6-1.el6.noarch
salt-repo-2016.11-2.el6.noarch
salt-master-2016.11.6-1.el6.noarch


** 针对Saltstack的在线安装  **

<!-- * 测试环境salt-master 192.168.3.167 用户名root 密码R00t@123

# Salt master 安装 #
```
#curl -L https://bootstrap.saltstack.com -o install_salt.sh
#sh install_salt.sh -P -M
``` -->
# 安装yum源
## el7
```
sudo yum install https://repo.saltstack.com/yum/redhat/salt-repo-2016.11-2.el7.noarch.rpm 
sudo yum clean expire-cache
```
## el6
```
yum install https://repo.saltstack.com/yum/redhat/salt-repo-2016.11-2.el6.noarch.rpm
```

# 安装saltstack相关软件(根据需求安装,不需全装)
```
sudo yum install salt-master
sudo yum install salt-minion
sudo yum install salt-api
sudo yum install salt-ssh
sudo yum install salt-syndic
sudo yum install salt-cloud
```

# salts master 配置 #
```
修改/etc/salt/master <默认端口ports 4505 and 4506>
interface: 192.168.3.167
重启salt-master
#service salt-master restart
```
> 该值以后加入自动运维平台的配置页面

# salt minion 安装 #
```
#curl -L https://bootstrap.saltstack.com -o install_salt.sh
#sh install_salt.sh -P
```

# salt minion 配置 #
```
配置/etc/salt/minion
master: 192.168.3.167
重启salt-minion
#service salt-minion restart
```

# salt key 配置 #
```
#salt-key --list-all
#salt-key --accept=<key>
#salt-key --accept-all
```

# 远程执行 #

## 测试salt minion 是否监听 ##
```
# salt '*' test.ping
cobbler:
    True
saltstack:
    True
```

## 运行shell命令 ##
```
# salt '*' cmd.run 'df -h'
saltstack:
    Filesystem                        Size  Used Avail Use% Mounted on
    /dev/mapper/vg_saltstack-lv_root   18G  3.4G   13G  21% /
    tmpfs                             940M  104K  940M   1% /dev/shm
    /dev/sda1                         485M   39M  421M   9% /boot
cobbler:
    Filesystem                           Size  Used Avail Use% Mounted on
    /dev/mapper/vg_cobbler-lv_root        27G   11G   14G  45% /
    tmpfs                                939M   16K  939M   1% /dev/shm
    /dev/sda1                            485M   40M  420M   9% /boot
    /root/CentOS-6.7-x86_64-minimal.iso  395M  395M     0 100% /mnt
[root@saltstack ~]#
```

## 执行 salt execution function ##
```
# salt '*' disk.usage
# salt '*' pkg.install cowsay
# salt '*' network.interfaces
```
## 针对特定主机执行 ##
1. Grains
```
salt -G 'os:Ubuntu' test.ping
```
2. Expression
```
salt -E 'minion[0-9]' test.ping
```
3. 指定客户端
```
salt -L 'minion1,minion2' test.ping
```
4. 复合条件
```
salt -C 'G@os:Ubuntu and minion* or S@192.168.50.*' test.ping
```
> \*S表示子网

# 创建 state #
> 默认state文件存放与/srv/salt目录下

创建一个nettools.sls文件
```
install_network_packages:
  pkg.installed:
    - pkgs:
      - lftp
```

执行命令<测试执行加 test=True>
```
# salt 'cobbler' state.apply nettools
cobbler:
----------
          ID: install_network_packages
    Function: pkg.installed
      Result: True
     Comment: The following packages were installed/updated: lftp
     Started: 15:44:26.489244
    Duration: 20637.681 ms
     Changes:   
              ----------
              lftp:
                  ----------
                  new:
                      4.0.9-14.el6
                  old:

Summary for cobbler
------------
Succeeded: 1 (changed=1)
Failed:    0
------------
Total states run:     1
Total run time:  20.638 s
```
> State module参考：https://docs.saltstack.com/en/latest/ref/states/all/

# cmd.script #
```
master上创建文件夹，脚本放置在该文件夹下
mkdir -p /srv/salt/scripts/
salt cobbler cmd.script salt://scripts/test.sh
cobbler:
   ----------
   pid:
       14882
   retcode:
       0
   stderr:
   stdout:

```

# 命令帮助查看#
```
salt cobbler sys.list_modules
salt cobbler sys.list_functions cmd
salt cobbler sys.doc cmd
```

# pillar #
