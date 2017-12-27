## install redis

### 安装rpm源
```
mv /etc/yum.repos.d/epel.repo /etc/yum.repos.d/epel.repo.backup

mv /etc/yum.repos.d/epel-testing.repo /etc/yum.repos.d/epel-testing.repo.backup

wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
```

### 安装redis
```
yum install -y redis
```
### 设置开机启动
```
systemctl enable redis.service
```

### 启动redis
```
systemctl start redis.service
```

### 查看启动状态
```
systemctl status redis.service
```