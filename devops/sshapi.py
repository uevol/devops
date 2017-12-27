#!/usr/bin/python
import paramiko

def remote_cmd(cmd,host,port=22,user='root',passwd='P@ssw0rd',timeout=30):
    ret = {'status':True,'result':'','err':''}
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host,port=int(port),username=user,password=passwd,timeout=timeout)
        stdin,stdout,stderr = ssh.exec_command(cmd)
        ret['result'] = stdout.read()
        ret['err'] = stderr.read()
    except Exception as e:
        ret = {'status':False,'err':str(e)}
    finally:
        ssh.close()
        return ret

def put_file(host, user, passwd, localpath, remotepath, port=22):
    ret = {'status':True, 'err':''}
    try:
        t = paramiko.Transport((host, int(port)))
        t.connect(username=user, password=passwd)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(localpath, remotepath)
    except Exception as e:
        ret = {'status':False, 'err':str(e)}
    return ret