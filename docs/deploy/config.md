# 部署及配置文档（centos 7.2.1511）

#### 主要软件及版本

    1. python 2.7
    2. django 1.11+
    3. mongodb 3.2 +
    4. saltstack 2016-11
    5. mysql或者其他数据库(支持django)

#### 操作系统设置

###### 1. 关闭selinux(设置为disabled)
```
# 查看selinux状态
sestatus

# 设置selinux为disabled(重启后生效)
vi /etc/selinux/config
...

SELINUX=disabled

...

# 如果不想重启，修改后执行以下命令
setenforce 0
```

###### 2. 配置静态DNS解析
```
echo "IP devops" >> /etc/hosts # 将IP替换成实际IP地址, 请不要更改devops,后续IP都会被devops替换
```

#### 软件安装

###### 1. Git安装
    
```
yum install -y git
```
     
###### 2. pip安装及安装源配置

```
yum install -y python-setuptools
easy_install -i http://pypi.douban.com/simple pip

mkdir -p  ~/.pip/
vi ~/.pip/pip.conf

[global]
index-url = http://pypi.douban.com/simple
trusted-host = pypi.douban.com
```  
    
###### 3. 安装mysql数据库

*如果只是测试，可以使用sqlite3，无需安装mysql数据库*

```
yum install -y mariadb mariadb-server
```

*设置开机启动*
```
systemctl enable mariadb.service
```

*启动数据库*
```
systemctl start mariadb.service
```

*查看数据库是否启动*
```
[root@localhost ~]# netstat -nlpat | grep 3306
tcp        0      0 0.0.0.0:3306            0.0.0.0:*               LISTEN      9699/mysqld
```

###### 4. 安装redis数据库

```
# 安装源
mv /etc/yum.repos.d/epel.repo /etc/yum.repos.d/epel.repo.backup

mv /etc/yum.repos.d/epel-testing.repo /etc/yum.repos.d/epel-testing.repo.backup

wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
```

```
# 安装redis
yum install -y redis
```

```
# 设置开机启动
systemctl enable redis.service
```

```
# 启动redis
systemctl start redis.service
```

```
# 查看启动状态
systemctl status redis.service
```

###### 5. 安装mongodb数据库
*下载mongodb数据库*
```
curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-3.6.1.tgz
```

*配置及启动数据库*
```
# 创建相关文件夹
mkdir -p /root/mongo/{data,etc,log}

# 创建mongodb用户
useradd -d /opt/mongo mongod

# 设置权限
chown -R mongod:mongod /opt/mongo

# 解压源码
tar xvf mongodb-linux-x86_64-rhel70-3.6.1.tgz -C /opt/mongo
mv /opt/mongo/mongodb-linux-x86_64-rhel70-3.6.1/* /opt/mongo
rm -rf /opt/mongo/mongodb-linux-x86_64-rhel70-3.6.1

# 添加mongo bin目录到系统PATH变量
vi /etc/profile

export MONGO_HOME=/opt/mongo
PATH=$PATH:$MONGO_HOME/bin

# 新建配置文件
vi /opt/mongo/etc/mongod.conf

systemLog:
  destination: file
  path: /root/mongo/log/mongo.log
  logAppend: true
storage:
  dbPath: /root/mongo/data
processManagment:
  fork: true
net:
  bindIp: devops # 默认是 127.0.0.1
      
# 新增 mongodb.service文件
vi /lib/systemd/system/mongodb.service

[Unit]  
  
Description=mongodb   
After=network.target remote-fs.target nss-lookup.target  
  
[Service]  
Type=forking  
ExecStart=/opt/mongo/bin/mongod --config /opt/mongo/etc/mongod.conf  
ExecReload=/bin/kill -s HUP $MAINPID  
ExecStop=/opt/mongo/bin/mongod --shutdown --config /opt/mongo/etc/mongod.conf  
PrivateTmp=true  
    
[Install]  
WantedBy=multi-user.target 

# 设置权限
chmod 644 /lib/systemd/system/mongodb.service

*启动关闭服务，设置开机启动*
# 启动服务  
systemctl start mongodb.service    
# 关闭服务    
systemctl stop mongodb.service    
# 开机启动    
systemctl enable mongodb.service 

*查看数据库是否启动*
[root@localhost ~]# netstat -nlapt | grep 27017
tcp        0      0 127.0.0.1:27017         0.0.0.0:*               LISTEN      9885/mongod
```

###### 6. 安装Apache
*安装*
```
yum install -y httpd
```

*配置开机启动*
```
systemctl enable httpd.service
```

*启动Apache*
```
systemctl start httpd.service
```

*查Apache是否启动*
```
[root@localhost ~]# netstat -nlapt | grep 80
tcp6       0      0 :::80                   :::*                    LISTEN      9993/httpd
```

###### 7. 安装及配置salt-master、salt-api
请查看[安装文档](https://github.com/uevol/devops/tree/master/docs/saltstack)

[salt-master安装](https://github.com/uevol/devops/blob/master/docs/saltstack/saltstack.md)

[salt-api安装配置](https://github.com/uevol/devops/blob/master/docs/saltstack/salt_rest_api.md)


#### devops安装配置

###### 1. clone代码
```
git clone https://github.com/uevol/devops.git
```

###### 2. 安装所需python库
```
yum -y install python-devel libxml2-devel libxslt-devel gcc openssl openssl-devel MySQL-python

cd /path/to/devops
pip install -r requirements.txt
```

###### 3. 设置数据库(mysql)
#### 创建数据库
```
mysql
create database devops default charset=utf8;
```

#### 创建用户
```
grant all on devops.* to devops@'%' identified by "devops";
```

###### 4. 修改django配置文件settings.py
```
# 根据实际情况修改以下配置项(以下是按生产配置)


DEBUG = False
ALLOWED_HOSTS = ['*']

# 数据库配置
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'devops',  
        'USER': 'devops',  
        'PASSWORD': 'devops',  
        'HOST': 'devops',
        'PORT': '3306',
    }
}

# 配置mongo数据库
MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASS = 'devops', 27017, '', ''

# 配置zabbix API用户和密码
ZABBIX_SERVER, ZABBIX_PORT, ZABBIX_PATH, ZABBIX_USER, ZABBIX_PASS = 'devops', 80, "/zabbix", "Admin", "zabbix"

# 配置salt api
SALT_IP, SALT_PORT, SALT_USER, SALT_PASSWD = 'devops', '8080', 'salt_api', 'salt_api'

# 配置rq队列
RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        # 'PASSWORD': 'some-password',
        'DEFAULT_TIMEOUT': 360,
    },
    'high': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        # 'PASSWORD': 'some-password',
        'DEFAULT_TIMEOUT': 120,
    },
    'low': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        # 'PASSWORD': 'some-password',
        'DEFAULT_TIMEOUT': 360,
    }
}

import django_rq
# get scheduler for rq_scheduler
scheduler = django_rq.get_scheduler('default')

# 配置静态文件路径
STATIC_ROOT = os.path.join(BASE_DIR, 'collectedstatic')
```

###### 5. 数据库迁移
```
cd /path/to/devops
python manage.py migrate
```

###### 6. 收集静态资源
```
python manage.py collectstatic
```

###### 7. 配置wsgi
```
mkdir /path/to/devops/wsgi
cd /path/to/devops/wsgi
vi wsgi.py # 复制粘贴如下内容
```

    import os
    import sys
    import django.core.handlers.wsgi
    from django.conf import settings
    from django.core.wsgi import get_wsgi_application

    # Add this file path to sys.path in order to import settings
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devops.settings")

    sys.stdout = sys.stderr

    DEBUG = False

    application = get_wsgi_application()
    
###### 8. 配置httpd
```
# 安装软件
yum install -y httpd-devel
yum install -y mod_wsgi

cd /etc/httpd/conf.d
vi /etc/httpd/conf.d/devops.conf # 复制粘贴如下内容并修改
```

```
# 根据实际情况修改端口
Listen 9000
<VirtualHost *:9000>
LoadModule  wsgi_module modules/mod_wsgi.so

# 根据实际情况修改路径(/path/to/devops)
WSGIScriptAlias / /opt/devops/wsgi/django.wsgi
Alias /static/ /opt/devops/collectedstatic/

# 需修改成实际ip地址
ServerName devops
#ServerAlias www.example.com

<Directory /opt/devops/collectedstatic/>
Options Indexes  FollowSymLinks
AllowOverride None
Require all granted
</Directory>

<Directory /opt/devops/wsgi>
Require all granted
</Directory>
ErrorLog   /etc/httpd/logs/ops.error.log
LogLevel info
</VirtualHost>
```

```
# 设置目录和文件权限
# 一般目录权限设置为 755，文件权限设置为 644 
cd /opt/devops
chmod -R 644 devops
find devops -type d | xargs chmod 755

# 设置logs文件夹的所有者
cd /opt/devops
chown -R apache:apache logs

# 设置media文件夹的所有者
cd /opt/devops
chown -R apache:apache media
```

###### 9. 初始化数据库
```
cd /path/to/devops
python manage.py shell < scripts/init_db.py
```

###### 10. 启动服务
```
# 重启httpd
systemctl restart httpd

# 查看httpd状态
[root@devops devops]# netstat -nlpat | grep httpd
tcp6       0      0 :::9000                 :::*                    LISTEN      43735/httpd
tcp6       0      0 :::80                   :::*                    LISTEN      43735/httpd
```

###### 11. 登录
```
http://172.16.171.155:9000  
初始账户及密码：admin/admin@123
```


#### salt-event(通过api解析salt event)、rq队列及rq_scheduler需单独启动
###### 1. 配置salt-event
```
# 新增 mongodb.service文件
vi /usr/lib/systemd/system/salt-event.service

[Unit]
Description=salt-event Service
After=salt-api.service

[Service]
Type=forking
ExecStart=/bin/sh -c 'nohup /usr/bin/python /opt/devops/scripts/monitor_salt_event/forward_to_devops.py >/dev/null  2>&1 &'
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
StandardOutput=syslog
StandardError=inherit

[Install]
WantedBy=multi-user.target 

# 设置权限
chmod 644 /usr/lib/systemd/system/salt-event.service

# 启动服务  
systemctl start salt-event.service    
# 关闭服务    
systemctl stop salt-event.service    
# 开机启动    
systemctl enable salt-event.service 

# 查看服务是否启动
[root@devops ~]# ps aux | grep forward_to_devops | grep -v grep
root       5699  0.0  0.6 312112 23736 ?        S    15:19   0:00 /usr/bin/python /opt/devops/scripts/monitor_salt_event/forward_to_devops.py
```

###### 2. 配置rq队列
```
# 新增 rqworker.service文件
vi /usr/lib/systemd/system/rqworker.service

[Unit]
Description=rqworker Service
After=redis.service

[Service]
Type=forking
ExecStart=/bin/sh -c 'nohup /usr/bin/rqworker high default low >/dev/null  2>&1 &'
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
StandardOutput=syslog
StandardError=inherit

[Install]
WantedBy=multi-user.target

# 设置权限
chmod 644 /usr/lib/systemd/system/rqworker.service

# 启动服务  
systemctl start rqworker.service    
# 关闭服务    
systemctl stop rqworker.service    
# 开机启动    
systemctl enable rqworker.service 

查看服务是否启动
[root@devops ~]# ps aux | grep rqworker | grep -v grep
root       9610  0.0  0.3 216808 13720 ?        S    16:13   0:00 /usr/bin/python /usr/bin/rqworker high default low
```

###### 3. 配置rq_scheduler服务
```
# 新增 rqscheduler.service文件
vi /usr/lib/systemd/system/rqscheduler.service

[Unit]
Description=rqscheduler Service
After=rqworker.service

[Service]
Type=forking
ExecStart=/bin/sh -c 'nohup /usr/bin/rqscheduler >/dev/null  2>&1 &'
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
StandardOutput=syslog
StandardError=inherit

[Install]
WantedBy=multi-user.target

# 设置权限
chmod 644 /usr/lib/systemd/system/rqscheduler.service

# 启动服务  
systemctl start rqscheduler.service   
# 关闭服务    
systemctl stop rqscheduler.service  
# 开机启动    
systemctl enable rqscheduler.service 

查看服务是否启动
[root@devops ~]# systemctl status rqscheduler
● rqscheduler.service - rqscheduler Service
   Loaded: loaded (/usr/lib/systemd/system/rqscheduler.service; disabled; vendor preset: disabled)
   Active: active (running) since Mon 2018-01-08 16:22:50 CST; 2s ago
  Process: 10208 ExecStart=/bin/sh -c nohup /usr/bin/rqscheduler >/dev/null  2>&1 & (code=exited, status=0/SUCCESS)
 Main PID: 10209 (rqscheduler)
   CGroup: /system.slice/rqscheduler.service
           └─10209 /usr/bin/python /usr/bin/rqscheduler

Jan 08 16:22:50 devops systemd[1]: Starting rqscheduler Service...
Jan 08 16:22:50 devops systemd[1]: Started rqscheduler Service.
[root@devops ~]#
[root@devops ~]# ps aux | grep rqscheduler | grep -v grep
root      10209  0.1  0.3 213332 12920 ?        S    16:22   0:00 /usr/bin/python /usr/bin/rqscheduler
```




