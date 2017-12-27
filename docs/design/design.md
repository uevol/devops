# 装机管理
## 主机硬件信息
```
物理服务器硬件信息采集通过LiveCD启动后自动执行post_server_info.sh实现,
该脚本位于cobbler服务器的/var/www/cobbler/svc/目录下.
LiveCD启动后，根据/etc/rc.local调用该脚本
```

## 服务器RAID
```
服务器加载LiveCD后，通过预先封装在镜像内的raid工具（HPSSACLI或者MegaCLI）实现
```
> ** 未解决：post_server_info.sh还未实现抓取磁盘、RAID、网卡信息 **

## 系统安装
```
选中已经初始化完成的系统，关联相应的操作系统（profile）,默认系统会自动分配一个IP地址，
提交后该系统信息会显示到<物理机系统安装>
```

## 配置
```
1. 系统镜像导入
2. cobbler关键配置
3. DHCP地址池管理
```

