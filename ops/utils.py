# -*- coding: utf-8 -*-
###
# author: wei.yang@jinmuinfo.com
# date : 2017-09-06
###
from devops.settings import SALTMASTER_IP, SALTMASTER_PORT, SALTMASTER_USER, SALTMASTER_PASSWD
from devops.settings import SALT_IP, SALT_PORT, SALT_USER, SALT_PASSWD
from devops.settings import mongo as MONGO_CLIENT
from ops.saltapi import SaltAPI
from .models import File
import time
import os
import json
from devops.sshapi import put_file

def exacute_cmd(user, client, target, arg_list):
	result = {}
	error = ''
	try:
		salt = SaltAPI(SALT_IP, SALT_USER, SALT_PASSWD, port=SALT_PORT)
		result = salt.run(fun='cmd.run', target=target, arg_list=arg_list)
		job = {'user':user, 'time':time.strftime("%Y-%m-%d %X", time.localtime()), 'client':client, \
		'target':target, 'fun':'cmd.run', 'arg':arg_list, \
		'status':'', 'progress':'Finish', 'result': str(result), 'cjid':str(int(round(time.time() * 1000)))}
		MONGO_CLIENT.devops.joblist.insert_one(job)
	except Exception as e:
		error = str(e)
	return result, error

def push_file_to_minion(user, client, target, arg_list):
	result = {}
	error = ''
	try:
		arg_list[0] = 'salt://files/' + arg_list[0]
		salt = SaltAPI(SALT_IP, SALT_USER, SALT_PASSWD, port=SALT_PORT)
		result = salt.run(fun='cp.get_file', target=target, arg_list=arg_list)
		job = {'user':user, 'time':time.strftime("%Y-%m-%d %X", time.localtime()), 'client':client, \
		'target':target, 'fun':'push file to minion', 'arg':' '.join(arg_list), \
		'status':'', 'progress':'Finish', 'result': str(result), 'cjid':str(int(round(time.time() * 1000)))}
		MONGO_CLIENT.devops.joblist.insert_one(job)
	except Exception as e:
		error = str(e)
	return result, error

def upload_file(file, destination="/tmp"):
	# result = False
	error = ''
	try:
		f = open(os.path.join(destination, file.name), 'wb+') 
		for chunk in file.chunks():
			f.write(chunk)  
		f.close()
		if "tar" in file.name:
			os.system('tar xvf %s -C %s'%(os.path.join(destination, file.name), destination))
			os.remove(os.path.join(destination, file.name))
		# res = put_file(SALTMASTER_IP, SALTMASTER_USER, SALTMASTER_PASSWD, \
		# os.path.join(destination, file.name), "/srv/salt/files")
		# if res['err']:
		# 	error = res['err']
	except Exception as e:
		error = str(e)
	return error

def get_file_from_minion(user, client, target, arg_list):
	result = {}
	error = ''
	try:
		salt = SaltAPI(SALT_IP, SALT_USER, SALT_PASSWD, port=SALT_PORT)
		result = salt.run(fun='cp.push', target=target, arg_list=arg_list)
		job = {'user':user, 'time':time.strftime("%Y-%m-%d %X", time.localtime()), 'client':client, \
		'target':','.join(target), 'fun':'get file from minion', 'arg':' '.join(arg_list), \
		'status':'', 'progress':'Finish', 'result': str(result), 'cjid':str(int(round(time.time() * 1000)))}
		MONGO_CLIENT.devops.joblist.insert_one(job)
	except Exception as e:
		error = str(e)
	return result, error

def run_script(user, client, target, arg_list, async=False):
	result = {}
	error = ''
	try:
		arg_list = 'salt://scripts/' + arg_list
		salt = SaltAPI(SALT_IP, SALT_USER, SALT_PASSWD, port=SALT_PORT)
		if async:
			result = salt.run_async(fun='cmd.script', target=target, arg_list=arg_list)
			job = {'user':user, 'time':time.strftime("%Y-%m-%d %X", time.localtime()), 'client':client, \
			'target':target, 'fun':'cmd.script', 'arg':arg_list, 'progress':'', 'jid':result['jid']}
		else:
			result = salt.run(fun='cmd.script', target=target, arg_list=arg_list)
			job = {'user':user, 'time':time.strftime("%Y-%m-%d %X", time.localtime()), 'client':client, \
			'target':target, 'fun':'cmd.script', 'arg':arg_list, \
			'status':'', 'progress':'Finish', 'result': str(result), 'cjid':str(int(round(time.time() * 1000)))}
		MONGO_CLIENT.devops.joblist.insert_one(job)
	except Exception as e:
		error = str(e)
	return result, error

def state_deploy(user, client, target, arg_list, async=False):
	result = {}
	error = ''
	try:
		arg_list = 'states/' + arg_list
		salt = SaltAPI(SALT_IP, SALT_USER, SALT_PASSWD, port=SALT_PORT)
		if async:
			result = salt.run_async(fun='state.sls', target=target, arg_list=arg_list)
			job = {'user':user, 'time':time.strftime("%Y-%m-%d %X", time.localtime()), 'client':client, \
			'target':target, 'fun':'state.sls', 'arg':arg_list, 'progress':'', 'jid':result['jid']}
		else:
			ret = salt.run(fun='state.sls', target=target, arg_list=arg_list)
			result = {}
			for key,value in ret.items():
				tmp = {'process':{}, 'summary':{}}
				succeeded = 0
				failed = 0
				total_duration = 0
				for k,v in value.items():
					tmp1 = k.split('_|-')
					fun = '.'.join([tmp1[0], tmp1[3]])
					v['fun'] = fun
					v['id'] = tmp1[1]
 					tmp['process'].update({str(v['__run_num__']):v})
					if v['result'] == True:
						succeeded += 1
					else:
						failed += 1
					total_duration += v['duration']
				tmp['summary'].update({'succeeded':succeeded, 'failed':failed, 'total_duration':total_duration})
				result[key] = tmp
			job = {'user':user, 'time':time.strftime("%Y-%m-%d %X", time.localtime()), 'client':client, \
			'target':target, 'fun':'state.sls', 'arg':arg_list, \
			'status':'', 'progress':'Finish', 'result': str(result), 'cjid':str(int(round(time.time() * 1000)))}
		MONGO_CLIENT.devops.joblist.insert_one(job)
	except Exception as e:
		error = str(e)
	return result, error