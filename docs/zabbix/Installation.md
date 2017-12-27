Installation from packages (rhel7 and mysql5.7)

1 Installing repository configuration package
```
rpm -ivh http://repo.zabbix.com/zabbix/3.0/rhel/7/x86_64/zabbix-release-3.0-1.el7.noarch.rpm
```

2 Installing Zabbix packages
### Install Zabbix packages. Example for Zabbix server and web frontend with mysql database
```
yum install zabbix-server-mysql zabbix-web-mysql
```

### installing Zabbix agent only
```
yum install zabbix-agent
```

3 Creating initial database

### install database (mysql)
```
wget https://dev.mysql.com/get/mysql57-community-release-el7-8.noarch.rpm
rpm -ivh mysql57-community-release-el7-8.noarch.rpm
yum install mysql-community-server -y
```
### 启动MySQL
```
service mysqld start
```
A superuser account 'root'@'localhost is created. A password for the superuser is set and stored in the error log file. To reveal it, use the following command:
```
grep 'temporary password' /var/log/mysqld.log
mysql -u root -p temporary password
```
### 修改root用户的密码：
```
ALERT USER 'root'@'localhost' IDENTIFIED BY 'R00t@123';
```

for mysql 5.6

1.关闭mysql
```
service mysql/mysqld stop（是mysql还是mysqld取决于你在chkconfig开机启动中添加的名字，可以使用chkconfig --list显示）
```
2、跳过权限启动
mysql的bin目录下使用：
```
mysqld_safe --skip-grant-table &
```
3、mysql -u root mysql
```
mysql>UPDATE user SET Password=PASSWORD('newpassword') where USER='root';
mysql>FLUSH PRIVILEGES;
```

4 、也可以使用此方法更改
```
mysqladmin -u root password 'new-password' 
```

建立Zabbix数据库及Zabbix用户
```
mysql> create database zabbix character set utf8 collate utf8_bin;
mysql> grant all privileges on zabbix.* to zabbix@localhost identified by 'zabbix';
mysql> flush privileges;
mysql> quit;
```

Create zabbix database and user on MySQL. For instructions on doing that, see database creation scripts for MySQL.
Then import initial schema and data.
```
cd /usr/share/doc/zabbix-server-mysql-3.0.0
zcat create.sql.gz | mysql -uroot -p zabbix
```
4 Starting Zabbix server process

Edit database configuration in zabbix_server.conf
```
vi /etc/zabbix/zabbix_server.conf
DBHost=localhost
DBName=zabbix
DBUser=zabbix
DBPassword=zabbix
```

Start Zabbix server process.
```
systemctl start zabbix-server
```
设置开机启动
```
chkconfig zabbix-server on
```
5 Editing PHP configuration for Zabbix frontend

Apache configuration file for Zabbix frontend is located in /etc/httpd/conf.d/zabbix.conf. Some PHP settings are already configured.
```
php_value max_execution_time 300
php_value memory_limit 128M
php_value post_max_size 16M
php_value upload_max_filesize 2M
php_value max_input_time 300
php_value always_populate_raw_post_data -1
# php_value date.timezone Europe/Riga
```
It's necessary to uncomment the “date.timezone” setting and set the right timezone for you. After changing the configuration file restart the apache web server.

```
systemctl start httpd
```

Zabbix frontend is available at http://zabbix-frontend-hostname/zabbix in the browser. Default username/password is Admin/zabbix.



zabbix_agent:

1 Installing repository configuration package
```
rpm -ivh http://repo.zabbix.com/zabbix/3.0/rhel/7/x86_64/zabbix-release-3.0-1.el7.noarch.rpm
```

2 Installing Zabbix packages

installing Zabbix agent only
```
yum install zabbix-agent
```


3 /etc/zabbix/zabbix_agentd.conf
```
# sed -i "s/Server=127.0.0.1/Server=192.168.3.171/" zabbix_agentd.conf
# sed -i "s/ServerActive=127.0.0.1/ServerActive=192.168.3.171:10051/" zabbix_agentd.conf 
# sed -i "s/# UnsafeUserParameters=0/UnsafeUserParameters=1/" zabbix_agentd.conf
```
4 service zabbix-agent start
 ```
chkconfig zabbix-agent on
```
如果zabbix-agent服务无法开启，报错 cannot set resource limit: [13] Permission denied
需要关闭selinux服务，方法如下：
```
＃sed -i  "s/SELINUX=enforcing/SELINUX=disabled/“ /etc/selinux/config
# setenforce 0
```