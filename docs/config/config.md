# 自动化运维平台

## 1、从github下载开发代码

### 安装git(如果已安装，请跳过改步)
```
yum install git
```

### clone开发代码
```
git clone https://github.com/uevol/opsp.git
```

## 2、配置python开发库

### 方法1、直接从网络安装
#### 配置pip豆瓣源(可选,可以有效提升安装速度)
```
mkdir -p  ~/.pip/pip.conf
vi pip.conf

[global]
index-url = http://pypi.douban.com/simple
trusted-host = pypi.douban.com
```

#### 安装python开发库
```
cd opsp/ops/
pip install -r requirements.txt
```
#### 实际测试在pip install之前以下软件需提前安装：
``` 
yum -y install python-devel libxml2-devel libxslt-devel gcc openssl openssl-devel MySQL-python
```

### 方法2、直接从已有环境copy库到新环境
```cd /usr/lib64/python2.7  
mv site-packages site-packages.bak  
mv usr_lib64_python2.7_site-packages.tar /usr/lib64/python2.7  
tar xvf /usr/lib64/python2.7/usr_lib64_python2.7_site-packages.tar  

cd /usr/lib/python2.7  
mv site-packages site-packages.bak  
mv usr_lib_python2.7_site-packages.tar /usr/lib/python2.7  
tar xvf /usr/lib/python2.7/usr_lib_python2.7_site-packages.tar
```

## 3、配置settings.py文件(根据实际情况修改配置)
```
cp ops/settings.py.template ops/settings.py
```

## 4、设置数据库

### 如果只是测试，可直接使用内置开发数据库(sqlite3)

#### 修改opsp配置文件settings.py的数据库配置：
```
DATABASES = {  
    'default': { 
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), 
    }  
} 
```

### for postgresql

#### 切换用户
```
su postgres
psql -U postgres 
```

#### 修改密码(可选)：
```
\password postgres  
```

#### 创建数据库用户dbuser，并设置密码:
```
CREATE USER ops WITH PASSWORD 'ops@123';  
```

#### 创建用户数据库，这里为opsdb，并指定所有者为ops:
```
CREATE DATABASE ops OWNER ops;  
```

#### 将opsdb数据库的所有权限都赋予ops，否则ops只能登录控制台，没有任何数据库操作权限:
```
GRANT ALL PRIVILEGES ON DATABASE opsdb to ops;  
```

#### 登录数据库
```
psql -U ops -d opsdb -h 127.0.0.1 -p 5432;  
```

#### 根据实际修改opsp配置文件settings.py的数据库配置：

```
DATABASES = {  
    'default': { 
        'ENGINE': 'django.db.backends.psql',  
        'NAME': 'opsdb',  
        'USER': 'ops',  
        'PASSWORD': 'ops@123',  
        'HOST': '192.168.31.200',  
        'PORT': '5432',  
    }  
} 
```

### for mysql

#### install MySQLdb
```
yum install -y MySQL-python
```

#### create db
```
mysql
create database devops default charset=utf8;
```

#### create user
```
grant all on devops.* to devops@'%' identified by "devops";
```

#### 根据实际修改opsp配置文件settings.py的数据库配置：

```
DATABASES = {  
    'default': { 
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'devops',  
        'USER': 'devops',  
        'PASSWORD': 'devops',  
        'HOST': 'localhost',
        'PORT': '3306',  
    }  
} 
```

## 5、数据库迁移
```cd ops
python manage.py migrate
```

## 6、初始化数据
```
cd opsp/ops/
python manage.py shell < scripts/init_db.py
```

## 7、启动服务
```
cd opsp/ops/
nohup python manage.py runserver 0.0.0.0:8000 & 
(启动后当前文件夹下自动生成nohup.out,可tailf nohup.out查看运行日志)
``` 

## 8、登录
```
http://xxxx.xxxx.xxxx.xxxx:8000  
初始账户及密码：admin/admin@123
```
