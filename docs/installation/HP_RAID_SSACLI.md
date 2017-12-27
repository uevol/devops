HP Raid工具ssacli的使用
LiveCD启动之后ssh登录，root用户的密码P@ssw0rd

ssacli安装在LiveCD的目录
/opt/ssacli/bin/ssacli



常用命令如下：
查看raid卡信息(包括控制器状态、Cache状态、电池状态)
# ssacli ctrl all show status

查看raid详细信息
# ssacli ctrl slot=0 show config detail

查看raid状态
# ssacli ctrl slot=0 ld all show

查看slot 0 阵列A 所有逻辑驱动器信息
# ssacli ctrl slot=0 array A ld all show

查看slot 0 阵列A 所有物理驱动器信息
# ssacli ctrl slot=0 array A pd all show

查看硬盘
# ssacli ctrl slot=0 pd all show status  //查看物理硬盘状态
# ssacli ctrl slot=0 pd all show  //查看物理硬盘

创建raid10
# ssacli ctrl slot=0 create type=ld drives=1I:1:3,1I:1:4,2I:1:5,2I:1:6 raid=1+0

用3，4，5号盘创建一个raid5阵列
# ssacli ctrl slot=0 create type=ld drives=1I:1:3,1I:1:4,2I:1:5 raid=5

创建raid1
# ssacli ctrl slot=1 create type=ld drives=1I:1:1-1I:1:2 raid=1 forced

删除raid
# ssacli ctrl slot=0 array A delete forced


​缓存：

​查看cache信息：
# ssacli ctrl all show config detail | grep -i cache

关闭物理磁盘cache
# ssacli ctrl slot=0 modify drivewritecache=disable

打开逻辑磁盘缓存
# ssacli ctrl slot=0 logicaldrive 2 modify caching=enable

在没有电池的情况下开启raid写缓存
# ssacli ctrl slot=0 modify nobatterywritecache=enable

设置读写百分比
# ssacli ctrl slot=0 modify cacheratio=10/90


指示灯：

打开array B磁盘的led灯
# ssacli ctrl slot=0 array B modify led=on
​
打开3号磁盘的led灯
# ssacli ctrl slot=0 pd 1I:1:3 modify led=on


收集日志
Ahs
Ilo web storage 页面截图
/var/log/messages and /var/log/dmesg
执行以下5条命令，将5个以logs开头的压缩包发给我。
ssacli ctrl all diag file=logs_logs.zip logs=on

ssacli ctrl all diag file=logs_xml.zip xml=on

ssacli ctrl all diag file=logs_ris.zip ris=on

ssacli ctrl all diag file=logs_zip.zip zip=on

ssacli ctrl all diag file=logs.zip

执行命令输出：

[root@livecd ~]# ssacli ctrl slot=0 create type=ld drives=1I:1:1,1I:1:2 raid=0
[root@livecd ~]#

创建成功没有输出


[root@livecd ~]# ssacli ctrl slot=0 create type=ld drives=1I:1:1,1I:1:2 raid=0

Error: This operation is not supported with the current configuration. Use the
       "show" command on devices to show additional details about the
       configuration.
Reason: Space for creation not available

创建失败有Error报错



[root@livecd ~]# ssacli ctrl slot=0 array A delete forced

Warning: Deleting an array can cause other array letters to become renamed.
         E.g. Deleting array A from arrays A,B,C will result in two remaining
         arrays A,B ... not B,C

删除成功有Warning：



[root@livecd ~]# ssacli ctrl slot=0 array A delete forced

Error: Controller identified by "slot=0" does not have an array identified by
       "A".

删除失败有Error
