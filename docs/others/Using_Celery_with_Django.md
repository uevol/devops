# Using_Celery_with_Django.md

## 软件及版本
```
django 1.11
celery 4.02
redis  3.2.3
python-redis 2.10.5
```

## 1. create a new proj/proj/celery.py module that defines the Celery instance
```
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('proj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
```

## 2. import this app in your proj/proj/__init__.py module
```
from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ['celery_app']
```

## 3. create demoapp/tasks.py
```
# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)
```

## 4. Celery settings in django.settings
```
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
```

## 5. 在APP目录下，如目录下添加如下 tasks.py
```
#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from celery import shared_task
# import time
# from celery import task


# @task()
@shared_task
def add(x, y):
    return x + y

# @task
@shared_task
def run_test_suit(ts_id):
    print "++++++++++++++++++++++++++++++++++++"
    print('jobs[ts_id=%s] running....' % ts_id)
    time.sleep(10.0)
    print('jobs[ts_id=%s] done' % ts_id)
    result = True
    return result
```

## 6. 在views视图中，添加相关视图
```
from django.http import HttpResponse
from .tasks import run_test_suit


def tasks(request):
    print('before run_test_suit')
    result = run_test_suit.delay('110')
    print('after run_test_suit')
    return HttpResponse("job is runing background~")
```

## 7. 添加url映射

## 8. 启动django server

## 9. celery -A proj worker -l info
proj是项目名称
启动成功界面如下：
```
[root@dev ops]# celery -A ops worker -l info
/usr/lib/python2.7/site-packages/celery/platforms.py:793: RuntimeWarning: You're running the worker with superuser privileges: this is
absolutely not recommended!

Please specify a different user using the -u option.

User information: uid=0 euid=0 gid=0 egid=0

  uid=uid, euid=euid, gid=gid, egid=egid,
 
 -------------- celery@dev v4.0.2 (latentcall)
---- **** ----- 
--- * ***  * -- Linux-3.10.0-327.el7.x86_64-x86_64-with-centos-7.2.1511-Core 2017-07-06 00:11:39
-- * - **** --- 
- ** ---------- [config]
- ** ---------- .> app:         ops:0x1582750
- ** ---------- .> transport:   redis://localhost:6379//
- ** ---------- .> results:     redis://localhost:6379/
- *** --- * --- .> concurrency: 2 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** ----- 
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery
                

[tasks]
  . installation.tasks.add
  . installation.tasks.run_test_suit
  . ops.celery.debug_task

[2017-07-06 00:11:39,794: INFO/MainProcess] Connected to redis://localhost:6379//
[2017-07-06 00:11:39,798: INFO/MainProcess] mingle: searching for neighbors
[2017-07-06 00:11:40,807: INFO/MainProcess] mingle: all alone
[2017-07-06 00:11:40,812: WARNING/MainProcess] /usr/lib/python2.7/site-packages/celery/fixups/django.py:202: UserWarning: Using settings.DEBUG leads to a memory leak, never use this setting in production environments!
  warnings.warn('Using settings.DEBUG leads to a memory leak, never '
[2017-07-06 00:11:40,813: INFO/MainProcess] celery@dev ready.
```

## 10. 浏览器访问之前设置的url测试celery异步执行




