# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from cmdb.models import CiCategory
from .utils import exacute_cmd,upload_file,push_file_to_minion,get_file_from_minion,run_script,state_deploy
import json
from devops.settings import mongo
import time
from devops.paginator import my_paginator
from .models import File
# Create your views here.

def RemoteCmdView(request):
    ''' remote exacute command '''
    if request.method == "POST":
        try:
            user = request.user.username
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                client =  request.META['HTTP_X_FORWARDED_FOR']  
            else:
                client = request.META['REMOTE_ADDR']
            hosts = request.POST.getlist('hosts', [])
            command = request.POST.get('command', '') if request.POST.get('command', '') else 'hostname'
            result, error = exacute_cmd(user, client, hosts, command)
            if error:
                res = {'code': 0, 'msg': str(error)}
            else:
                res = {'code': 1, 'msg': '执行成功', "result": result}
        except Exception as e:
            res = {'code': 0, 'msg': str(error)}
    return render(request, 'command/remote_cmd.html', locals())

def SelectHostView(request):
    ''' select host '''
    category = get_object_or_404(CiCategory, code='host')
    items = category.ciproperty_set.filter(is_search=True)
    return render(request, 'command/select_host.html', locals())

def JobListView(request):
    ''' job list '''
    dt_till = int(time.time())
    interval = 60 * 60 * 24
    dt_from = dt_till - interval
    dt_till = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(dt_till))
    dt_from = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(dt_from))
    return render(request, 'job_result/job_list.html', locals())

def JobListViewAPI(request):
    ''' job list api '''
    if request.GET.get('dt_till',''):
        dt_till = request.GET.get('dt_till', '')
        dt_from = request.GET.get('dt_from', '')
    else:
        dt_till = int(time.time())
        interval = int(request.GET.get('interval','')) if request.GET.get('interval','') else 60 * 60 * 24
        dt_from = dt_till - interval
        dt_till = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(dt_till))
        dt_from = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(dt_from))
    if request.user.is_superuser:
        print dt_from, dt_till
        jobs = mongo.devops.joblist.find({'time': {'$gte': dt_from, '$lte': dt_till}}).sort([('_id',-1)])
    else:
        jobs = mongo.salt.joblist.find({'user':request.user.username, 'time': {'$gte': dt_from, '$lte': dt_till} }).sort([('_id',-1)])
    data = [{'user': job['user'], 'time': job['time'], 'client': job['client'], 'target': job['target'], 'fun': job['fun'], \
    'arg': job['arg'], 'progress': job['progress'], 'cjid': job['cjid'], 'status': job['status'] } for job in jobs ]
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    count, data = my_paginator(data, page, limit)
    
    res = {'code': 0, 'msg': '', 'count': count, 'data': data}
    return JsonResponse(res)

def JobResultView(request,cjid):
    job = mongo.devops.joblist.find_one({'cjid':cjid})
    if job.has_key('fun') and job['fun'] == 'cmd.script':
        result = {}
        for minion,ret in eval(job['result']).items():
            result[minion] = {'stderr':ret['stderr'],'stdout':ret['stdout']}
        return render(request,'job_result/show_job_result.html',locals())
    elif job.has_key('fun') and job['fun'] == 'state.sls':
        result = eval(job['result'])
        for k,v in result.items():
            process = collections.OrderedDict(sorted(v['process'].iteritems(),key=lambda x:x[0]))
            summary = v['summary']
            result[k] = {'process':process,'summary':summary}
        return render(request,'job_result/show_state_result.html',locals())
    else:
        job['result'] = eval(job['result'])
        print job
        return render(request,'job_result/job_result.html',locals())   

def PushFileVifew(request):
    ''' push file to remote host(s) by saltstack '''
    if request.method == "POST":
        try:
            user = request.user.username
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                client =  request.META['HTTP_X_FORWARDED_FOR']  
            else:
                client = request.META['REMOTE_ADDR']
            hosts = request.POST.getlist('hosts', [])
            filename = request.POST.get('filename', '')
            remote_path = request.POST.get('remote_path', '')
            arg_list = [filename, remote_path, 'makedirs=True']
            result, error = push_file_to_minion(user, client, hosts, arg_list)
            if error:
                res = {'code': 0, 'msg': str(error)}
            else:
                res = {'code': 1, 'msg': '文件推送成功', "result": result}
        except Exception as e:
            res = {'code': 0, 'msg': str(error)}
    return render(request, 'file/file.html', locals())

def UploadFileVifew(request):
    ''' Upload file to remote salt-master server '''
    if request.method == "POST":
        try:
            file = request.FILES.get("file", None)
            user = request.user.username
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                client =  request.META['HTTP_X_FORWARDED_FOR']
            else:
                client = request.META['REMOTE_ADDR']
            myfile,updated = File.objects.update_or_create(code=file.name, name=file.name, defaults={'created_by':user})
            res = upload_file(file)
            if res:
                myfile.delete()
                res = {'code': 0, 'msg': res}
            else:
                res = {'code': 1, 'msg': '文件上传成功', 'filename': file.name }
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
    return JsonResponse(res)

def ScripListView(request):
    ''' script list '''
    return render(request, 'script/script_list.html', locals())

def ScripListViewAPI(request):
    ''' script list  API'''
    scripts = File.objects.all()
    data = [{'name': script.name, 'script_name': script.script_name, 'created_by': script.created_by, 'comment': script.comment, \
    'create_time': script.create_time, 'update_time': script.update_time} for script in scripts ]
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    count, data = my_paginator(data, page, limit)
      
    res = {'code': 0, 'msg': '', 'count': count, 'data': data}
    return JsonResponse(res)