# salt-api

This document is about configing rest salt api.

## 一. 安装Salt-API

### 1. PyPI
```
pip install salt-api
pip install cherrypy==3.2.3
chkconfig salt-api on # 设置开机启动
```

### 2. Rpm
```
yum install salt-api -y
chkconfig salt-api on
```

注：如果遇到以下报错，请将cherrypy换成3.2.3版本
Dec 15 12:22:01 localhost.localdomain salt-api[5659]: @cherrypy.exposed
Dec 15 12:22:01 localhost.localdomain salt-api[5659]: AttributeError: 'module' object has no attribute 'exposed'
```
pip install cherrypy==3.2.3
```


## 二. 配置Salt-API
### 1. 生成自签名证书(用于ssl)

```
cd  /etc/pki/tls/certs
# 生成自签名证书, 过程中需要输入key密码及RDNs
make testcert
cd /etc/pki/tls/private/
# 解密key文件，生成无密码的key文件, 过程中需要输入key密码，该密码为之前生成证书时设置的密码
openssl rsa -in localhost.key -out localhost_nopass.key
```

### 2. Salt-API配置

#### (1) 创建用于salt-api的用户
```
useradd -M -s /sbin/nologin salt_api
echo "salt_api" | passwd salt_api —stdin
```

#### (2) 配置eauth, /etc/salt/master.d/eauth.conf
```
external_auth:
  pam:
    salt_api:
      - .*
      - '@wheel'
      - '@runner'
```

#### (3) 配置Salt-API, /etc/salt/master.d/api.conf
```
rest_cherrypy:
  port: 8080
  ssl_crt: /etc/pki/tls/certs/localhost.crt
  ssl_key: /etc/pki/tls/private/localhost_nopass.key
```

#### (4) 启动Salt-API
```
service salt-api start
service salt-master restart
```

### 3. Salt-API使用
测试工具为操作系统自带的 curl

#### (1) Login

* Request

```
curl -k https://192.168.38.10:8000/login -H "Accept: application/x-yaml" \
     -d username='pengyao' \
     -d password='pengyao_pass' \
     -d eauth='pam'
```

* Response

```
return:
- eauth: pam
  expire: 1385579710.806725
  perms:
  - .*
  start: 1385536510.8067241
  token: 784ee23c63794576a50ca5d3d890eb71efb0de6f
  user: pengyao
```

其中 token 后边的串为认证成功后获取的token串，之后可以不用再次输入密码，直接使用本Token即可

#### (2) 查询Minion(minion-01.example.com)的信息

* Request

```
curl -k https://192.168.38.10:8000/minions/minion-01.example.com \
     -H "Accept: application/x-yaml" \
     -H "X-Auth-Token: 8e211da5d6bbb51fbffe6468a3ca0c6a24b3e535"
```
其中 X-Auth-Token 后边的串为之前Login获取到的Token串, 如果请求的URL不包含 minion-01.example.com ，则请求的为所有Minion的信息

* Response

```
return:
- minion-01.example.com:
    cpu_flags:
    - fpu
    - vme
    - de
    ......
```

#### (3) job管理

获取缓存的jobs列表

* Request

```
curl -k https://192.168.38.10:8000/jobs/ \
     -H "Accept: application/x-yaml" \
     -H "X-Auth-Token: 8e211da5d6bbb51fbffe6468a3ca0c6a24b3e535"
```

* Response

```
return:
- '20131127065003726179':
    Arguments: []
    Function: test.ping
    Start Time: 2013, Nov 27 06:50:03.726179
    Target: '*'
    Target-type: glob
    User: sudo_vagrant
```

#### (4) 查询指定的job

* Request

```
curl -k https://192.168.38.10:8000/jobs/20131127065003726179 \
     -H "Accept: application/x-yaml" \
     -H "X-Auth-Token: 8e211da5d6bbb51fbffe6468a3ca0c6a24b3e535"
```

* Response

```
return:
- minion-01.example.com: true
```

#### (5) 远程执行模块

* Request

```
curl -k https://192.168.38.10:8000/ \
     -H "Accept: application/x-yaml" \
     -H "X-Auth-Token: 8e211da5d6bbb51fbffe6468a3ca0c6a24b3e535" \
     -d client='local' \
     -d tgt='*' \
     -d fun='test.ping'
```
也可以请求 https://192.168.38.10:8000/run ，不过该方法为一次性使用，无法使用Token, 只能使用username和password

* Response

```
return:
- minion-01.example.com: true
```

#### (6) 运行runner

* Request

```
curl -k https://192.168.38.10:8000/ \
     -H "Accept: application/x-yaml" \
     -H "X-Auth-Token: 8e211da5d6bbb51fbffe6468a3ca0c6a24b3e535" \
     -d client='runner' \
     -d fun='manage.status'
```

* Response

```
return:
- down: []
  up:
  - minion-01.example.com
```

#### (7) 运行wheel

注意: 由于当前版本的Salt Master有一处bug, 导致wheel的结果无法返回(https://groups.google.com/forum/#!topic/salt-users/9HcZ6R7MB0g)，官方在最新的代码中已经修复,使用时需要使用github中最新的salt代码

* Request(例子为查询所有的minion key列表)

```
curl -k https://localhost:8000/ \
     -H "Accept: application/x-yaml" \
     -H "X-Auth-Token: 8e211da5d6bbb51fbffe6468a3ca0c6a24b3e535" \
     -d client='wheel' \
     -d fun='key.list_all'
```

* Response

```
return:
- data:
    _stamp: 2013-12-23_04:54:22.483159
    fun: wheel.key.list_all
    jid: '20131223045422481844'
    return:
      local:
      - master.pem
      - master.pub
      minions:
      - minion-01.example.com
      minions_pre: []
      minions_rejected: []
     success: true
     tag: salt/wheel/20131223045422481844
     user: pengyao
   tag: salt/wheel/20131223045422481844
```

#### (8) Targeting


如果想在api中使用salt的 Targeting 功能，可以在Request的Post Data中增加 expr_form (默认是 glob )及值即可:

依然以curl为例:

```
curl -k https://192.168.38.10:8000/ \
     -H "Accept: application/x-yaml" \
     -H "X-Auth-Token: 8e211da5d6bbb51fbffe6468a3ca0c6a24b3e535" \
     -d client='local' \
     -d tgt='webcluster' \
     -d expr_form='nodegroup' \
     -d fun='test.ping'
```

将利用 nodegroup 匹配到名为 webcluster 的target。