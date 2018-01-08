需要手动增加可以远程访问数据库的用户。

## 方法一、本地登入mysql，更改 "mysql" 数据库里的 "user" 表里的 "host" 项，将"localhost"改为"%"
```
mysql -u root -proot
mysql>use mysql;
mysql>update user set host = '%' where user = 'root';
mysql>select host, user from user;
FLUSH PRIVILEGES
```

## 方法二、直接授权(推荐)
　　从任何主机上使用root用户，密码：youpassword（你的root密码）连接到mysql服务器：
```
mysql -u root -proot 
mysql>GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'youpassword' WITH GRANT OPTION;
FLUSH PRIVILEGES
```

## 操作完后切记执行以下命令刷新权限 
FLUSH PRIVILEGES 