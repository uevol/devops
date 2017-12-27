# reactor
> 通过监测minion start event触发reactor，采集grains信息

## 配置reactor
```
#cat /etc/salt/master.d/reactor.conf
reactor:
  - 'salt/key':
    - /srv/reactor/first_grains.sls
  - 'salt/minion/*/start':
    - /srv/reactor/getgrains.sls
  - 'salt/auth':
    - /srv/reactor/auto_sign.sls
```

## 配置采集grains的sls

### 1. cat /srv/reactor/getgrains.sls

```
getgrains.sls:
  local.grains.items:
    - tgt: {{ data['id'] }}
```

### 2. cat /srv/reactor/first_grains.sls
```
{% if 'act' in data and data['act'] == 'accept' %}
first_grains:
  local.grains.items:
    - tgt: {{ data['id'] }}
{% endif %}
```

## 配置自动签核
```
vi auto_sign.sls

{% if 'act' in data and data['act'] == 'pend' %}
minion_add:
  wheel.key.accept:
    - match: {{ data['id'] }}
{% endif %}
```