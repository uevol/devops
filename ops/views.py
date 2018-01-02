# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from cmdb.models import CiCategory
from .utils import exacute_cmd, upload_file, push_file_to_minion, get_file_from_minion, run_script, state_deploy
import json
from devops.settings import mongo
import time
from devops.paginator import my_paginator
from .models import File
from django.db.models import Q
import collections
from devops.decorators import permission_check
from devops.settings import scheduler
# Create your views here.

@permission_check(['run_cmd'])
def RemoteCmdView(request):
    ''' remote exacute command '''
    if request.method == "POST":
        try:
            user = request.user.username
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                client =  request.META['HTTP_X_FORWARDED_FOR']  
            else:
                client = request.META['REMOTE_ADDR']
            hosts = request.POST.get('hosts', [])
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
        jobs = mongo.devops.joblist.find({'time': {'$gte': dt_from, '$lte': dt_till}}).sort([('_id',-1)])
    else:
        jobs = mongo.devops.joblist.find({'user':request.user.username, 'time': {'$gte': dt_from, '$lte': dt_till} }).sort([('_id',-1)])
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
        return render(request,'job_result/job_script_result.html',locals())
    elif job.has_key('fun') and job['fun'] == 'state.sls':
        result = eval(job['result'])
        for k,v in result.items():
            process = collections.OrderedDict(sorted(v['process'].iteritems(),key=lambda x:x[0]))
            summary = v['summary']
            result[k] = {'process':process,'summary':summary}
        return render(request,'job_result/job_state_result.html',locals())
    else:
        job['result'] = eval(job['result'])
        return render(request,'job_result/job_result.html',locals())   

@permission_check(['push_file'])
def PushFileVifew(request):
    ''' push file to remote host(s) by saltstack '''
    if request.method == "POST":
        try:
            user = request.user.username
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                client =  request.META['HTTP_X_FORWARDED_FOR']  
            else:
                client = request.META['REMOTE_ADDR']
            hosts = request.POST.get('hosts', '')
            filename = request.POST.get('filename', '')
            remote_path = request.POST.get('remote_path', '')
            arg_list = [filename, remote_path, 'makedirs=True']
            # arg_list = [filename, remote_path]
            result, error = push_file_to_minion(user, client, hosts, arg_list)
            if error:
                res = {'code': 0, 'msg': str(error)}
            else:
                res = {'code': 1, 'msg': '文件推送成功', "result": result}
        except Exception as e:
            res = {'code': 0, 'msg': str(error)}
    return render(request, 'file/file.html', locals())

@permission_check(['upload_file'])
def UploadFileVifew(request):
    ''' Upload file to remote salt-master server '''
    if request.method == "POST":
        try:
            file = request.FILES.get("file", None)
            file_type = request.POST.get('file_type', '')
            user = request.user.username
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                client =  request.META['HTTP_X_FORWARDED_FOR']
            else:
                client = request.META['REMOTE_ADDR']
            if file_type == 'other':
                myfile,updated = File.objects.update_or_create(code=file.name, name=file.name, defaults={'created_by':user})
                res = upload_file(file, '/srv/salt/files')
            elif file_type == 'script':
                myfile,updated = File.objects.update_or_create(code=file.name, name=file.name, \
                    file_type='script', defaults={'created_by':user})
                res = upload_file(file, '/srv/salt/scripts')
            else:
                myfile,updated = File.objects.update_or_create(code=file.name, name=file.name, \
                    file_type='state', defaults={'created_by':user})
                res = upload_file(file, '/srv/salt/states')
            if res:
                myfile.delete()
                res = {'code': 0, 'msg': res}
            else:
                res = {'code': 1, 'msg': '文件上传成功', 'filename': file.name }
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
    return JsonResponse(res)

@permission_check(['delete_file'])
def FileDeleteView(request, pk=''):
    ''' Delete file '''
    try:
        File.objects.filter(pk=pk).delete()
        res = {'code': 1, 'msg': '删除成功 ！'}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    return JsonResponse(res)

def ScriptListView(request):
    ''' script list '''
    return render(request, 'script/script_list.html', locals())

def ScriptListViewAPI(request):
    ''' script list  API'''
    keyword = request.GET.get('keyword', '')
    if keyword:
        q = Q(code__icontains=keyword) | Q(name__icontains=keyword)
        scripts = File.objects.filter(file_type='script').filter(q)
    else:
        scripts = File.objects.filter(file_type='script')
    data = [{'id': script.id, 'code': script.code, 'name': script.name, 'file_type': script.file_type, 'created_by': script.created_by, \
    'comment': script.comment, 'create_time': script.create_time, 'update_time': script.update_time} for script in scripts ]
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    count, data = my_paginator(data, page, limit)
      
    res = {'code': 0, 'msg': '', 'count': count, 'data': data}
    return JsonResponse(res)

def ScriptEditView(request, pk=''):
    try:
        script = File.objects.get(pk=pk)
        file = '/srv/salt/scripts/' + script.code
        f = open(file,'r')
        context = f.read()
        f.close()
    except Exception as e:
        context = str(e)
    return render(request,'script/show_script.html',locals())

def ScriptRunView(request, pk=''):
    script = File.objects.get(pk=pk)
    if request.method == "POST":
        try:
            hosts = request.POST.get('hosts')
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                client =  request.META['HTTP_X_FORWARDED_FOR']  
            else:
                client = request.META['REMOTE_ADDR']
            user = request.user.username
            result, error = run_script(user, client, hosts, script.code)
            if error:
                res = {'code': 0, 'msg': str(error)}
            else:
                res = {'code': 1, 'msg': '执行成功', "result": result}
        except Exception as e:
            res = {'code': 0, 'msg': str(error)}
    return render(request,'script/run_script.html',locals())

def StateListView(request):
    ''' salt state list '''
    return render(request, 'state/state_list.html')

def StateListViewAPI(request):
    ''' script list  API'''
    keyword = request.GET.get('keyword', '')
    if keyword:
        q = Q(code__icontains=keyword) | Q(name__icontains=keyword)
        scripts = File.objects.filter(file_type='state').filter(q)
    else:
        scripts = File.objects.filter(file_type='state')
    data = [{'id': script.id, 'code': script.code, 'name': script.name, 'file_type': script.file_type, 'created_by': script.created_by, \
    'comment': script.comment, 'create_time': script.create_time, 'update_time': script.update_time} for script in scripts ]
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    count, data = my_paginator(data, page, limit)
      
    res = {'code': 0, 'msg': '', 'count': count, 'data': data}
    return JsonResponse(res)

@permission_check(['run_state'])
def StateRunView(request, pk=''):
    script = File.objects.get(pk=pk)
    if request.method == "POST":
        try:
            hosts = request.POST.get('hosts')
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                client =  request.META['HTTP_X_FORWARDED_FOR']  
            else:
                client = request.META['REMOTE_ADDR']
            user = request.user.username
            res, error = state_deploy(user, client, hosts, script.code.split('.')[0])
            if error:
                result = {'code': 0, 'msg': str(error)}
            else:
                result = {'code': 1, 'msg': '执行成功', "result": res}
        except Exception as e:
            result = {'code': 0, 'msg': str(error)}
    return render(request,'state/run_state.html',locals())

def CronListView(request):
    return render(request,'cron/cron_list.html',locals())

def CronListAPIView(request):
    job_instances = scheduler.get_jobs()
    data = [{'id':job.id, 'cron_string':job.meta['cron_string'], 'targets':','.join(job.args[2]), \
    'arg':job.args[3], 'created_at':job.created_at.strftime("%Y-%m-%d %H:%M:%S"), \
    'last_exacuted':job.ended_at.strftime("%Y-%m-%d %H:%M:%S") if job.ended_at else ''} for job in job_instances]
    
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    count, data = my_paginator(data, page, limit)
      
    res = {'code': 0, 'msg': '', 'count': count, 'data': data}
    return JsonResponse(res)

def CronAddView(request):
    if request.method == 'POST':
        cron_string = request.POST.get('cron_string', '')
        cron_type = request.POST.get('cron_type', '')
        try:
            user = 'cron'
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                client =  request.META['HTTP_X_FORWARDED_FOR']  
            else:
                client = request.META['REMOTE_ADDR']
            arg_list = request.POST.get('cmd', '') if request.POST.get('cmd', '') else 'echo hello'
            hosts = request.POST.get('hosts', '')
            target = hosts.split(',')
            print cron_string, cron_type, arg_list, hosts
            if cron_type == 'command':
                job = scheduler.cron(cron_string, func=exacute_cmd, args=[user, client, target, arg_list], repeat=None, queue_name='default')
            else:
                job = scheduler.cron(cron_string, func=run_script, args=[user, client, target, arg_list, True], repeat=None, queue_name='default')
            if job:
                res = {'code': 1, 'msg': '任务创建成功 ！'}
            else:
                res = {'code': 0, 'msg': '任务创建失败 ！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    return render(request,'cron/cron_add.html',locals())

def CronDeleteView(request,job_id):
    try:
        scheduler.cancel(job_id)
        res = {'code': 1, 'msg': '定时任务已经删除'}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    return JsonResponse(res)
































