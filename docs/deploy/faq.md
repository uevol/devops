部署中遇到的问题

###### 1. 配置完成后，发现salt不可用，出现如下错误
```
[root@devops ~]# journalctl -xe
Jan 05 15:29:45 devops salt-master[11576]: File "/usr/lib/python2.7/site-packages/salt/crypt.py", line 52, in <
Jan 05 15:29:45 devops salt-master[11576]: import salt.transport.client
Jan 05 15:29:45 devops salt-master[11576]: File "/usr/lib/python2.7/site-packages/salt/transport/client.py", li
Jan 05 15:29:45 devops salt-master[11576]: from salt.utils.async import SyncWrapper
Jan 05 15:29:45 devops salt-master[11576]: File "/usr/lib/python2.7/site-packages/salt/utils/async.py", line 8,
Jan 05 15:29:45 devops salt-master[11576]: import tornado.ioloop
Jan 05 15:29:45 devops salt-master[11576]: File "/usr/lib64/python2.7/site-packages/tornado/ioloop.py", line 47
Jan 05 15:29:45 devops salt-master[11576]: from tornado.concurrent import TracebackFuture, is_future
Jan 05 15:29:45 devops salt-master[11576]: File "/usr/lib64/python2.7/site-packages/tornado/concurrent.py", lin
Jan 05 15:29:45 devops salt-master[11576]: from tornado.log import app_log
Jan 05 15:29:45 devops salt-master[11576]: File "/usr/lib64/python2.7/site-packages/tornado/log.py", line 37, i
Jan 05 15:29:45 devops salt-master[11576]: from tornado.escape import _unicode
Jan 05 15:29:45 devops salt-master[11576]: File "/usr/lib64/python2.7/site-packages/tornado/escape.py", line 27
Jan 05 15:29:45 devops salt-master[11576]: from tornado.util import unicode_type, basestring_type, u
Jan 05 15:29:45 devops salt-master[11576]: ImportError: cannot import name u
Jan 05 15:29:45 devops systemd[1]: salt-master.service: main process exited, code=exited, status=64/n/a
Jan 05 15:29:45 devops systemd[1]: Failed to start The Salt Master Server.
-- Subject: Unit salt-master.service has failed
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
--
-- Unit salt-master.service has failed.
--
-- The result is failed.
Jan 05 15:29:45 devops systemd[1]: Unit salt-master.service entered failed state.
Jan 05 15:29:45 devops systemd[1]: salt-master.service failed.
Jan 05 15:29:45 devops polkitd[917]: Unregistered Authentication Agent for unix-process:11561:713858 (system bu
lines 2563-2589/2589 (END)
```

解决方法：
```
重新安装tornado
pip uninstall tornado
pip install tornado
```


