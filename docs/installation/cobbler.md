# cobbler install(Centos 6.5)
## Disable selinux
```
vi /etc/selinux/config
```
## Install cobbler
```
rpm -Uvh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
yum install cobbler
```
## Change settings(/etc/cobbler/settings)
### Default Encrypted Password
#### Change the password
```
[root@cobbler cobbler]# openssl passwd -1
Password: 
Verifying - Password: 
$1$.11OEPXh$w/N2aagIG86Awd0xCzZQP/
```
#### Put the new password between the "" below
```
default_password_crypted: "$1$.11OEPXh$w/N2aagIG86Awd0xCzZQP/"
```

### Server and Next_Server
#### Server
The server option sets the IP that will be used for the address of the cobbler server. DO NOT use 0.0.0.0, as it is not the listening address.
```
server: 172.16.171.194
```

#### Next_Server
if using cobbler with manage_dhcp, put the IP address
of the cobbler server here so that PXE booting guests can find it
```
next_server: 172.16.171.194
```
### DHCP Management and DHCP Server Template
In order to PXE boot, you need a DHCP server to hand out addresses and direct the booting system to the TFTP server where it can download the network boot files. Cobbler can manage this for you, via the manage_dhcp setting:
```
 # default, don't manage
manage_dhcp: 0
```
Change that setting to 1 so cobbler will generate the dhcpd.conf file based on the dhcp.template that is included with cobbler. This template will most likely need to be modified as well, based on your network settings:
```
$ vi /etc/cobbler/dhcp.template
```
For most uses, you'll only need to modify this block:
```
subnet 192.168.1.0 netmask 255.255.255.0 {
     option routers             192.168.1.1;
     option domain-name-servers 192.168.1.210,192.168.1.211;
     option subnet-mask         255.255.255.0;
     filename                   "/pxelinux.0";
     default-lease-time         21600;
     max-lease-time             43200;
     next-server                $next_server;
}
```
No matter what, make sure you do not modify the "next-server $next_server;" line, as that is how the next_server setting is pulled into the configuration. This file is a cheetah template, so be sure not to modify anything starting after this line:
```
 #for dhcp_tag in $dhcp_tags.keys():
```
### Files and Directory Notes
Cobbler makes heavy use of the /var directory. The /var/www/cobbler/ks_mirror directory is where all of the distribution and repository files are copied, so you will need 5-10GB of free space per distribution you wish to import.

### Starting and Enabling the Cobbler Service
Once you have updated your settings, you're ready to start the service. Fedora now uses systemctl to manage services, but you can still use the regular init script:
```
$ service cobblerd start
$ chkconfig cobblerd on
$ service cobblerd status
```
### Checking for Problems
Now that the cobblerd service is up and running, it's time to check for problems. Cobbler's check command will make some suggestions, but it is important to remember that these are mainly only suggestions and probably aren't critical for basic functionality. If you are running iptables or SELinux, it is important to review any messages concerning those that check may report.
```
[root@cobbler ~]# cobbler check
The following are potential configuration items that you may want to fix:

1 : dhcpd is not installed
2 : change 'disable' to 'no' in /etc/xinetd.d/tftp
3 : change 'disable' to 'no' in /etc/xinetd.d/rsync
4 : file /etc/xinetd.d/rsync does not exist
5 : debmirror package is not installed, it will be required to manage debian deployments and repositories
6 : ksvalidator was not found, install pykickstart
7 : fencing tools were not found, and are required to use the (optional) power management features. install cman or fence-agents to use them

Restart cobblerd and then run 'cobbler sync' to apply changes.
```
### Solve the problem for cobbler check
####[^1] Install DHCP
```
yum install dhcp
```

#### Change 'disable' to 'no' in /etc/xinetd.d/tftp

#### Touch /etc/xinetd.d/rsync and change 'disable' to 'no' in /etc/xinetd.d/rsync

### First Sync
```
[root@cobbler ~]# cobbler sync
task started: 2017-06-06_173553_sync
task started (id=Sync, time=Tue Jun  6 17:35:53 2017)
running pre-sync triggers
cleaning trees
removing: /var/lib/tftpboot/grub/images
copying bootloaders
trying hardlink /var/lib/cobbler/loaders/pxelinux.0 -> /var/lib/tftpboot/pxelinux.0
trying hardlink /var/lib/cobbler/loaders/menu.c32 -> /var/lib/tftpboot/menu.c32
trying hardlink /var/lib/cobbler/loaders/yaboot -> /var/lib/tftpboot/yaboot
trying hardlink /usr/share/syslinux/memdisk -> /var/lib/tftpboot/memdisk
trying hardlink /var/lib/cobbler/loaders/grub-x86_64.efi -> /var/lib/tftpboot/grub/grub-x86_64.efi
trying hardlink /var/lib/cobbler/loaders/grub-x86.efi -> /var/lib/tftpboot/grub/grub-x86.efi
copying distros to tftpboot
copying images
generating PXE configuration files
generating PXE menu structure
rendering DHCP files
generating /etc/dhcp/dhcpd.conf
rendering TFTPD files
generating /etc/xinetd.d/tftp
cleaning link caches
running post-sync triggers
running python triggers from /var/lib/cobbler/triggers/sync/post/*
running python trigger cobbler.modules.sync_post_restart_services
running: dhcpd -t -q
received on stdout: 
received on stderr: 
running: service dhcpd restart
received on stdout: Starting dhcpd: [  OK  ]

received on stderr: 
running shell triggers from /var/lib/cobbler/triggers/sync/post/*
running python triggers from /var/lib/cobbler/triggers/change/*
running python trigger cobbler.modules.scm_track
running shell triggers from /var/lib/cobbler/triggers/change/*
*** TASK COMPLETE ***
```

## Download an ISO Image
```
mount -o loop iso_dir/CentOS-6.8-x86_64-minimal.iso /mnt/vcdrom/
```
## Run the Import
```
[root@cobbler ~]# cobbler import --name=CentOS-6.8 --arch=x86_64 --path=/mnt/vcdrom/
task started: 2017-06-06_190931_import
task started (id=Media import, time=Tue Jun  6 19:09:31 2017)
Found a candidate signature: breed=redhat, version=rhel6
Found a matching signature: breed=redhat, version=rhel6
Adding distros from path /var/www/cobbler/ks_mirror/CentOS-6.8-x86_64:
creating new distro: CentOS-6.8-x86_64
trying symlink: /var/www/cobbler/ks_mirror/CentOS-6.8-x86_64 -> /var/www/cobbler/links/CentOS-6.8-x86_64
creating new profile: CentOS-6.8-x86_64
associating repos
checking for rsync repo(s)
checking for rhn repo(s)
checking for yum repo(s)
starting descent into /var/www/cobbler/ks_mirror/CentOS-6.8-x86_64 for CentOS-6.8-x86_64
processing repo at : /var/www/cobbler/ks_mirror/CentOS-6.8-x86_64
directory /var/www/cobbler/ks_mirror/CentOS-6.8-x86_64 is missing xml comps file, skipping
*** TASK COMPLETE ***
```
## Listing Objects
```
[root@cobbler ~]# cobbler distro list
   CentOS-6.8-x86_64
```
## list profiles
Profiles can be used to PXE boot, but most of the features in cobbler revolve around system objects. 
```
[root@cobbler ~]# cobbler profile list
   CentOS-6.8-x86_64
```
The import command will typically create at least one distro/profile pair, which will have the same name as shown above.

## Show Object Details
```
[root@cobbler ~]# cobbler distro report --name=CentOS-6.8-x86_64
Name                           : CentOS-6.8-x86_64
Architecture                   : x86_64
TFTP Boot Files                : {}
Breed                          : redhat
Comment                        : 
Fetchable Files                : {}
Initrd                         : /var/www/cobbler/ks_mirror/CentOS-6.8-x86_64/images/pxeboot/initrd.img
Kernel                         : /var/www/cobbler/ks_mirror/CentOS-6.8-x86_64/images/pxeboot/vmlinuz
Kernel Options                 : {}
Kernel Options (Post Install)  : {}
Kickstart Metadata             : {'tree': 'http://@@http_server@@/cblr/links/CentOS-6.8-x86_64'}
Management Classes             : []
OS Version                     : rhel6
Owners                         : ['admin']
Red Hat Management Key         : <<inherit>>
Red Hat Management Server      : <<inherit>>
Template Files                 : {}
```
## Creating a System
When creating a system, the name and profile are the only two required fields:
```
[root@cobbler ~]# cobbler system add --name=test --profile=CentOS-6.8-x86_64
[root@cobbler ~]# cobbler system list
   test
[root@cobbler ~]# cobbler system report --name=test
Name                           : test
TFTP Boot Files                : {}
Comment                        : 
Enable gPXE?                   : <<inherit>>
Fetchable Files                : {}
Gateway                        : 
Hostname                       : 
Image                          : 
IPv6 Autoconfiguration         : False
IPv6 Default Device            : 
Kernel Options                 : {}
Kernel Options (Post Install)  : {}
Kickstart                      : <<inherit>>
Kickstart Metadata             : {}
LDAP Enabled                   : False
LDAP Management Type           : authconfig
Management Classes             : <<inherit>>
Management Parameters          : <<inherit>>
Monit Enabled                  : False
Name Servers                   : []
Name Servers Search Path       : []
Netboot Enabled                : True
Owners                         : <<inherit>>
Power Management Address       : 
Power Management ID            : 
Power Management Password      : 
Power Management Type          : ipmitool
Power Management Username      : 
Profile                        : CentOS-6.8-x86_64
Internal proxy                 : <<inherit>>
Red Hat Management Key         : <<inherit>>
Red Hat Management Server      : <<inherit>>
Repos Enabled                  : False
Server Override                : <<inherit>>
Status                         : production
Template Files                 : {}
Virt Auto Boot                 : <<inherit>>
Virt CPUs                      : <<inherit>>
Virt Disk Driver Type          : <<inherit>>
Virt File Size(GB)             : <<inherit>>
Virt Path                      : <<inherit>>
Virt PXE Boot                  : 0
Virt RAM (MB)                  : <<inherit>>
Virt Type                      : <<inherit>>
```
## Edit system
The primary reason for creating a system object is network configuration. When using profiles, you're limited to DHCP interfaces, but with systems you can specify many more network configuration options.

So now we'll setup a single, simple interface in the 192.168.1/24 network:
```
$ cobbler system edit --name=test --interface=eth0 --mac=00:11:22:AA:BB:CC --ip-address=192.168.1.100 --netmask=255.255.255.0 --static=1 --dns-name=test.mydomain.com
```
The default gateway isn't specified per-NIC, so just add that separately (along with the hostname):
```
cobbler system edit --name=test --gateway=192.168.1.1 --hostname=test.mydomain.com
```

