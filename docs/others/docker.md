### docker安装mysql
#### 创建目录用于映射容器中的目录
```
mkdir -p /docker/mysql/{conf,logs,data}
```
data目录将映射为mysql容器配置的数据文件存放路径
logs目录将映射为mysql容器的日志目录
conf目录里的配置文件将映射为mysql容器的配置文件

#### 拉取官方镜像
```
docker pull mysql
```

#### 运行容器
```
cd /docker/mysql
docker run -p 3306:3306 --name=mysql -v $PWD/conf:/etc/mysql/mysql.conf.d -v $PWD/logs:/var/log/mysql -v $PWD/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=R00t@123 -e MYSQL_DATABASE=devops -e MYSQL_USER=devops -e MYSQL_PASSWROD=devops -d mysql
```


### docker安装mongodb
#### 创建目录用于映射容器中的目录
```
mkdir -p /docker/mongo/db
```
db目录将映射为mongo容器配置的数据文件存放路径

#### 拉取官方镜像
```
docker pull mongo
```

#### 运行容器
```
cd /docker/mongo
docker run -p 27017:27017 --name=mongo -v $PWD/db:/data/db -d mongo
```


### 
