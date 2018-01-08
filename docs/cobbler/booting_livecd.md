# LiveCD
## 安装制作环境
添加yum源：
```
[livecd]
name = CentOS $releasever - LiveCD
baseurl = http://www.nanotechnologies.qc.ca/propos/linux/centos-live/$basearch/live
enabled=1
protect=0
gpgkey = http://www.nanotechnologies.qc.ca/propos/linux/RPM-GPG-KEY-PGuay2010

yum install livecd-tools syslinux anaconda-runtime
```

## 编写kickstart脚本
```
vi centos-livecd-minimal.ks

lang en_US.UTF-8
keyboard us
timezone Asia/Shanghai
auth --useshadow --enablemd5
selinux --disabled
firewall --disabled

repo --name=a-base    --baseurl=https://mirrors.aliyun.com/centos/6.8/os/$basearch
repo --name=a-updates --baseurl=https://mirrors.aliyun.com/centos/6.8/updates/$basearch
repo --name=a-extras  --baseurl=https://mirrors.aliyun.com/centos/6.8/extras/$basearch
repo --name=a-live    --baseurl=http://www.nanotechnologies.qc.ca/propos/linux/centos-live/$basearch/live

%packages
bash
kernel
syslinux
passwd
policycoreutils
chkconfig
authconfig
rootfiles
comps-extras
xkeyboard-config
openssh
openssh-server
openssh-clients
```

## 开始制作Livecd
```
mkdir -p /root/tmp/{livecd,iso}
LANG=C livecd-creator --config=centos-livecd-minimal.ks --cache=/root/tmp/livecd/cache --tmpdir=/root/tmp/livecd/tmp --fslabel=LiveCD
```
## 定制Livecd
### 安装定制环境
```
yum install squashfs-tools
```
### 挂载ISO镜像
```
   mkdir -p /root/live/tmp
   mount -o loop -t iso9660 /root/live/LiveCD.iso /root/live/tmp
```
### copy镜像
```
mkdir -p /root/live/img
cp -R /root/live/tmp/* /root/live/img
```

### 解压squashfs.img
```
cd /root/live/img/LiveOS
unsquashfs squashfs.img
```
### 挂载ext3fs.img文件
```
cd /root/live/img/LiveOS/squashfs-root/LiveOS
mount -o loop,rw ext3fs.img /tmp/iso
```
### 定制修改系统后卸载
```
vi rc.local
....

umount /tmp/iso
```
### 生成新的squashfs.img文件,然后删除squashfs-root目录
```
cd /root/live/img/LiveOS
mksquashfs squashfs-root squashfs.img
rm -rf squashfs-root
```
### 回到上级目录，打包新的ISO
```
cd /root/live/img/
genisoimage -o /tmp/LiveCD.iso -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -R -J -v -V "LiveCDV1" -T ./
```

## pxeboot
```
livecd-iso-to-pxeboot LiveCD.iso
```
## Add distro to cobbler
```
mkdir -p /srv/livecd
cp /path/to/cwd/tftpboot/vmlinuz0 /srv/livecd/vmlinuz0
cp /path/to/cwd/tftpboot/initrd0.img /srv/livecd/initrd0.img
cp LiveCD.iso /srv/livecd

cobbler distro add --name=LiveCD --kernel=/srv/livecd/vmlinuz0 --initrd=/srv/livecd/initrd0.img --arch=x86_64
```

## Add profile to cobbler
```
cobbler profile add --name=LiveCD --distro=LiveCD
```
## Add system
```
cobbler system add --name=LiveCD --profile=LiveCD
```
