# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CiCategory, CiProperty
import json
from devops.paginator import my_paginator
from django.http import JsonResponse
from django.db.models import Q
from devops.settings import mongo
from json2html import *
from .zabbix_utils import *
import time
from django.contrib.auth.models import User, Group
from admins.models import Service
from devops.decorators import permission_check
from django.contrib.auth.decorators import login_required

# Create your views here.
@permission_check(['r_model'])
def CategoryListView(request):
    ''' configration category list views '''
    categories = CiCategory.objects.all()
    return render(request, 'ci_category/ci_category_list.html', locals())

@permission_check(['r_model'])
def CategoryListViewAPI(request):
    ''' configration category list view API '''
    # 查询处理
    category_id = request.GET.get('id', '')

    if category_id:
        categories = CiCategory.objects.filter(pk=category_id)
    else:
        categories = CiCategory.objects.all()
    data = [{'id': category.id, 'name': category.name, 'url': category.get_url(), 'comment': category.comment} for category in categories]

    # 分页处理
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    count, data = my_paginator(data, page, limit)

    res = {'code': 0, 'msg': '', 'count': count, 'data': data}
    return JsonResponse(res)

@permission_check(['c_model'])
def CategoryCreateView(request):
    ''' category create view '''
    if request.method == 'POST':
        try:
            post_data = {key: value for key, value in request.POST.iteritems() if value and key != 'csrfmiddlewaretoken'}
            CiCategory(**post_data).save()
            res = {'code': 1, 'msg': '模型已经创建！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    return render(request, 'ci_category/ci_category_form.html', locals())

@permission_check(['r_model'])
def CategoryDetailView(request, pk=''):
    ''' CategoryDetail '''
    category = get_object_or_404(CiCategory, pk=pk)
    return render(request, 'ci_category/ci_category_detail.html', locals())

@permission_check(['u_model'])
def CategoryUpdateView(request, pk=''):
    ''' CategoryUpdate '''
    if request.method == 'POST':
        try:
            post_data = {key: value for key, value in request.POST.iteritems() if key != 'csrfmiddlewaretoken'}
            post_data['show_in_left'] = request.POST.get('show_in_left', 0)
            CiCategory.objects.filter(pk=pk).update(**post_data)
            res = {'code': 1, 'msg': '模型已经更新！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    category = get_object_or_404(CiCategory, pk=pk)
    return render(request, 'ci_category/ci_category_update.html', locals())

@permission_check(['d_model'])
def CategoryDeleteView(request, pk=''):
    ''' CategoryDelete '''
    try:
        CiCategory.objects.filter(pk=pk).delete()
        res = {'code': 1, 'msg': '删除成功 ！'}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    return JsonResponse(res)

@permission_check(['c_field'])
def PropertyCreateView(request, category_pk=''):
    ''' create propery for someone category'''
    if request.method == 'POST':
        try:
            post_data = {key: value for key, value in request.POST.iteritems() if value and key != 'csrfmiddlewaretoken'}
            post_data['ci_category_id'] = int(category_pk)
            CiProperty.objects.create(**post_data)
            res = {'code': 1, 'msg': '模型属性已添加！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    form_type_choice = CiProperty.FORM_TYPE_CHOICE
    value_type_choice = CiProperty.VALUE_TYPE_CHOICE
    category = get_object_or_404(CiCategory, pk=category_pk)
    return render(request, 'ci_property/ci_property_create.html', locals())

@permission_check(['u_field'])
def PropertyUpdateView(request, pk=''):
    ''' update propery '''
    if request.method == 'POST':
        try:
            post_data = {key: value for key, value in request.POST.iteritems() if key != 'csrfmiddlewaretoken'}
            CiProperty.objects.filter(pk=pk).update(**post_data)
            res = {'code': 1, 'msg': '模型属性已经更新！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    ci_property = get_object_or_404(CiProperty, pk=pk)
    return render(request, 'ci_property/ci_property_update.html', locals())

@permission_check(['d_field'])
def PropertyDeleteView(request, pk=''):
    ''' PropertyDelete '''
    try:
        CiProperty.objects.filter(pk=pk).delete()
        res = {'code': 1, 'msg': '删除成功 ！'}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    return JsonResponse(res)

@csrf_exempt
def CreateOrUpdateHostAPI(request):
    ''' create or update host according to posted data from salt '''
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if data.get('api_type', '') == 'host_disk':
                host = mongo.devops.host.find_one({'minion_id': data['minion_id']})
                mongo.devops.host.update_one({'minion_id': data['minion_id']}, {'$set':data, "$currentDate": {"lastModified": True}})
                res = {'code': 0, 'o': 'update host disk'}
            else:
                host = mongo.devops.host.find_one({'server_id': data['server_id']})
                if host:
                    mongo.devops.host.update_one({'server_id': data['server_id']}, {'$set':data, "$currentDate": {"lastModified": True}})
                    res = {'code': 0, 'o': 'update'}
                else:
                    # data['tags'] = []
                    # data['env'] = ''
                    # data['admin'] = []
                    mongo.devops.host.insert_one(data)
                    res = {'code': 0, 'o': 'insert'}
        except Exception as e:
            res = {'code': 1, 'error': str(e)}
    else:
        res = {'code': 0, 'msg': 'test'}
    return JsonResponse(res)

@permission_check(['r_host'])
def HostListView(request):
    ''' host list view '''
    category = get_object_or_404(CiCategory, code='host')
    items = category.ciproperty_set.filter(is_search=True)
    return render(request, 'host/host_list.html', locals())

@permission_check(['r_host'])
def HostListViewAPI(request):
    ''' host list view API '''
    # 查询处理
    keyword = request.GET.get('keyword', '')
    if keyword:
        hosts = mongo.devops.host.find({'$or':[{'hostname': {'$regex': keyword, '$options': 'i'}}, {'ip': {'$regex': keyword}}]})
    else:
        get_data = { key: value for key, value in request.GET.iteritems() if value and (key not in ['csrfmiddlewaretoken', 'page', 'limit']) }
        if get_data:
            query_filter = {}
            for key, value in get_data.iteritems():
                name, value_type = key.split('-')
                if value_type == 'array':
                    query_filter[name] = {"$all": value.split(",")}
                else:
                    query_filter[name] = {'$regex': value, '$options': 'i'}
            hosts = mongo.devops.host.find(query_filter)
        else:
            hosts = mongo.devops.host.find({})
    data = []
    for host in hosts:
        s = host.pop("_id")
        data.append(host)

    # 分页处理
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    count, data = my_paginator(data, page, limit)

    res = {'code': 0, 'msg': '', 'count': count, 'data': data}
    return JsonResponse(res)

@permission_check(['u_host'])
def setTable(request):
    ''' set host fields that is showed in host list table '''
    category = get_object_or_404(CiCategory, code='host')
    if request.method == "POST":
        try:
            items = {key: True for key, value in request.POST.iteritems() if value and key != 'csrfmiddlewaretoken'}
            for item in category.ciproperty_set.all():
                if item.code in items.keys():
                    item.show_in_table = True
                else:
                    item.show_in_table = False
                item.save()
            res = {'code': 1, 'msg': '设置成功'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    return render(request, 'host/set_table.html', locals())

@permission_check(['r_host'])
def HostDetailView(request, server_id=''):
    host = mongo.devops.host.find_one({'server_id': server_id})
    eth = host.get('eth', '')
    if eth:
        eth = eval(eth)
        if "lo" in eth:
            eth.pop('lo')
        eth = json2html.convert(json = eth)
    category = get_object_or_404(CiCategory, code='host')
    items = category.ciproperty_set.filter(is_must=False)
    # custom_info = { item.code: {'name': item.name, 'value': host.get(item.code, '')} for item in items }
    custom_info = ((item.name, host.get(item.code, '')) for item in items)
    return render(request, 'host/host_detail.html', locals())

def zabbix(request,ip=''):
    if request.POST.get('dt_till',''):
        dt_till = time.mktime(time.strptime(request.POST.get('dt_till',''),'%Y-%m-%d %H:%M:%S'))
        dt_from = time.mktime(time.strptime(request.POST.get('dt_from',''),'%Y-%m-%d %H:%M:%S'))
    else:
        dt_till = time.time()
        interval = int(request.POST.get('interval','')) if request.POST.get('interval','') else 60 * 60 * 1
        dt_from = dt_till - interval
    graph_selected = request.POST.get('graph','') if request.POST.get('graph','') else 'CPU load'
    graphs = get_graph_by_ip(ip)
    if graphs:
        graphid = graphs[graph_selected]
        items = get_item_by_graphid(graphid)
        if items:
            legend,data = [],[]
            for key,itemid in items.items():
                legend.append(key)
                tmp = get_history_data(itemid,time_from=dt_from,time_till=dt_till)
                value,name = [],key
                for x in tmp:
                    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(x['clock'])))
                    value.append([date,x['value']])
                data.append({'value':value,'name':key})
            context = json.dumps({"legend":legend,"data":data})
    dt_from=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(dt_from))
    dt_till=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(dt_till))
    return render(request,'host/zabbix.html',locals())

def zabbix_refresh(request):
    ip = request.POST.get('ip','')
    dt_till = time.time()
    interval = request.POST.get('interval','')
    dt_from = dt_till - int(interval)
    graph_selected = request.POST.get('graph','') if request.POST.get('graph','') else 'CPU load'
    graphs = get_graph_by_ip(ip)
    if graphs:
        graphid = graphs[graph_selected]
        items = get_item_by_graphid(graphid)
        if items:
            data = []
            for key, itemid in items.items():
                tmp = get_history_data(itemid,time_from=dt_from,time_till=dt_till)
                for x in tmp:
                    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(x['clock'])))
                    data.append([date,x['value']])
            context = json.dumps({"data":data})
    dt_from=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(dt_from))
    dt_till=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(dt_till))
    return HttpResponse(context)

@permission_check(['u_host'])
def HostUpdateView(request, server_id=''):
    if request.method == "POST":
        try:
            post_data = {}
            for item in request.POST.keys():
                if item == 'csrfmiddlewaretoken':
                    continue
                else:
                    key, value_type = item.split('-')
                    if 'array' in value_type:
                        post_data[key] = request.POST.getlist(item, [])
                    else:
                        post_data[key] = request.POST.get(item, '')
            print post_data
            mongo.devops.host.update_one({'server_id': server_id},{'$set': post_data})  
            res = {'code': 1, 'msg': '已经更新！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)  
    host = mongo.devops.host.find_one({'server_id': server_id})
    category = get_object_or_404(CiCategory, code='host')
    items = category.ciproperty_set.all()
    # for admin
    admin = host.get('admin', [])
    users = (user.username for user in User.objects.all())
    admin_item = items.get(code='admin')
    # for tags
    tags = ','.join(host.get('tags', []))
    tags_item = items.get(code='tags')
    # for others
    not_edit_items = items.filter(is_edit=False)
    edit_items = items.filter(is_edit=True).exclude(code__in=['admin', 'tags'])
    not_edit_item_info = ((item.name, host.get(item.code, '')) for item in not_edit_items)
    edit_item_info = ((item.name, item.code, host.get(item.code, ''), item.form_type, item.value_type, \
    item.get_optional_value()) for item in edit_items)
    return render(request, 'host/host_update.html', locals())

@permission_check(['d_host'])
def HostDeleteView(request, server_id=''):
    ''' Delete host '''
    try:
        mongo.devops.host.remove({'server_id': server_id})
        res = {'code': 1, 'msg': '删除成功 ！'}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    return JsonResponse(res)

@permission_check(['c_host'])
def HostAddView(request):
    ftp = Service.objects.get(name='ftp')
    linux_script = "install-minion.sh"
    win_script = "install-minion.vbs"
    if ftp.path:
        url = "http://%s:%s/%s/"%(ftp.host, ftp.port, ftp.path)
    else:
        url = "http://%s:%s/"%(ftp.host, ftp.port)
    return render(request, 'host/add_host.html', locals())