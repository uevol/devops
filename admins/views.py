# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User, Group
from .models import *
from django.http import HttpResponse, JsonResponse
import datetime
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
import random, string
from django.contrib.auth import authenticate
from devops.paginator import my_paginator
from .models import Role, Perm, Service
from devops.decorators import permission_check
from django.contrib.auth.decorators import login_required
# Create your views here.

@permission_check(['r_user'])
def UserListView(request):
    ''' user list view '''
    roles = Role.objects.all()
    return render(request, 'user/user_list.html', locals())

@permission_check(['r_user'])
def UserListAPI(request):
    ''' user list api'''

    # 查询处理
    search_filter = request.GET.get('search_filter', '')
    role = request.GET.get('role', '')
    q = Q(username__icontains=search_filter) | Q(email__icontains=search_filter)
    if role:
        user_set = User.objects.select_related().filter(role__name__icontains=role).filter(q).distinct()
    else:
        user_set = User.objects.select_related().filter(q).distinct()

    # 构造返回数据结构
    user_list = []
    for user in user_set:
        roles = []
        for role in user.role_set.all():
            roles.append(role.name)
        user_instance = {'id': user.id, 'username': user.username, 'email': user.email, 'roles': roles, \
        'is_active': '已激活' if user.is_active else '未激活', 'phone': user.profile.phone, \
        'wechat': user.profile.wechat, 'comment': user.profile.comment, \
        'last_login': user.last_login + datetime.timedelta(hours=8) if user.last_login else user.last_login}
        user_list.append(user_instance)
    
    # 分页处理
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    count, data = my_paginator(user_list, page, limit)

    res = {'code': 0, 'msg': '', 'count': count, 'data': data}
    return JsonResponse(res)

@permission_check(['c_user'])
def UserCreateView(request): 
    ''' UserCreate '''
    roles = Role.objects.all()
    groups = Group.objects.all()
    if request.method == 'POST':
        try:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            email = request.POST.get('email', '')
            is_active = request.POST.get('is_active', 0)
            roles = request.POST.getlist('roles[]', '')
            groups = request.POST.getlist('groups[]', '')
            phone = request.POST.get('phone', '')
            wechat = request.POST.get('wechat', '')
            comment = request.POST.get('comment', '')
            user = User.objects.create(username=username, email=email, is_active=is_active)
            user.set_password(password)
            user.profile.phone = phone
            user.profile.wechat = wechat
            user.profile.comment = comment
            user.save()
            user.role_set = roles
            user.groups = groups
            res = {'code': 1, 'msg': '用户已经创建！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    return render(request, 'user/user_form.html', locals())

@permission_check(['u_user'])
def UserUpdateView(request, pk=1):
    ''' UserUpdate '''
    user = get_object_or_404(User, pk=pk)
    roles = Role.objects.all()
    groups = Group.objects.all()
    if request.method == 'POST':
        try:
            user.username = request.POST.get('username', '')
            user.email = request.POST.get('email', '')
            user.is_active = request.POST.get('is_active', 0)
            user.profile.phone = request.POST.get('phone', '')
            user.profile.wechat = request.POST.get('wechat', '')
            user.profile.comment = request.POST.get('comment', '')
            user.role_set = request.POST.getlist('roles[]', '')
            user.groups = request.POST.getlist('groups[]', '')
            user.save()
            res = {'code': 1, 'msg': '更新成功！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    return render(request, 'user/user_update.html', locals())

@permission_check(['u_user'])
def UserResetPdView(request, pk=1):
    ''' User resest password '''
    user = get_object_or_404(User, pk=pk)
    try:
        password = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        user.set_password(password)
        user.save()
        res = {'code': 1, 'msg': '重置成功！当前密码：%s'%(password)}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    return JsonResponse(res)

@login_required
def UserChangePdView(request, pk=1):
    ''' User change password '''
    if request.method == 'POST':
        user = get_object_or_404(User, pk=pk)
        try:
            old_password = request.POST.get('old_password', '')
            user = authenticate(username=request.user.username, password=old_password)
            if user:
                new_password = request.POST.get('new_password', '')
                new_password1 = request.POST.get('new_password1', '')
                if new_password == new_password1:
                    user.set_password(new_password)
                    user.save()
                    res = {'code': 1, 'msg': '修改密码成功'}
                else:
                    res = {'code': 0, 'msg': '两次输入密码不一致'}
            else:
                res = {'code': 0, 'msg': '旧密码错误'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    return render(request, 'user/user_change_pass.html')

@login_required
def UserDetailView(request, pk=1):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        try:
            user.email = request.POST.get('email', '')
            user.profile.phone = request.POST.get('phone', '')
            user.profile.wechat = request.POST.get('wechat', '')
            user.profile.comment = request.POST.get('comment', '')
            user.save()
            res = {'code': 1, 'msg': '更新成功！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    return render(request, 'user/user_detail.html', locals())

@permission_check(['d_user'])
def UserDeleteView(request, pk=1):
    ''' UserDelete '''
    try:
        if pk == 1:
            res = {'code': 0, 'msg': '超级管理员,禁止删除'}
        else:
            User.objects.filter(pk=pk).delete()
            res = {'code': 1, 'msg': '删除成功 ！'}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    return JsonResponse(res)

@permission_check(['r_user_group'])
def GroupListView(request):
    ''' user list view '''
    groups = Group.objects.all()
    return render(request, 'group/group_list.html', locals())

@permission_check(['r_user_group'])
def GroupSearchView(request):
    ''' group search '''
    search_filter = request.GET.get('search_filter', '')
    user_group = request.GET.get('user_group', '')
    all_group = Group.objects.all()
    q = Q(name__icontains=search_filter) | Q(user__username__icontains=search_filter)
    if user_group:
        groups = Group.objects.select_related().filter(name=user_group).filter(q).distinct()
    else:
        groups = Group.objects.select_related().filter(q).distinct()
    return render(request, 'group/group_list.html', locals())

@permission_check(['c_user_group'])
def GroupCreateView(request):
    ''' GroupCreate '''
    users = User.objects.all()
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '')
            uid_list = request.POST.getlist('users[]', '')
            group = Group.objects.create(name=name)
            group.user_set = uid_list
            res = {'code': 1, 'msg': '用户组已经创建！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    return render(request, 'group/group_form.html', locals())

@permission_check(['u_user_group'])
def DeleteUserFromGroup(request, gid='', uid=''):
    ''' remove user from group '''
    try:
        group = Group.objects.get(pk=gid)
        group.user_set.remove(uid)
        res = {'code': 1, 'msg': '该用户已从用户组删除'}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    return JsonResponse(res)

@permission_check(['u_user_group'])
def GroupUpdateView(request, pk=''):
    ''' GroupUpdate '''
    users = User.objects.all()
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        try:
            group.name = request.POST.get('name', '')
            group.save()
            group.user_set = request.POST.getlist('users[]', '')
            res = {'code': 1, 'msg': '用户组已经更新！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    return render(request, 'group/group_update.html', locals())

@permission_check(['d_user_group'])
def GroupDeleteView(request, pk=1):
    ''' GroupDelete '''
    try:
        if pk == 1:
            res = {'code': 0, 'msg': '管理员组,禁止删除'}
        else:
            Group.objects.filter(pk=pk).delete()
            res = {'code': 1, 'msg': '删除成功 ！'}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    return JsonResponse(res)

@permission_check(['r_role'])
def RoleListView(request):
    ''' user list view '''
    roles = Role.objects.all()
    return render(request, 'role/role_list.html', locals())

@permission_check(['c_role'])
def RoleCreateView(request):
    ''' RoleCreate '''
    users = User.objects.all()
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '')
            uid_list = request.POST.getlist('users[]', '')
            role = Role.objects.create(name=name)
            role.users = uid_list
            res = {'code': 1, 'msg': '角色已经创建！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    return render(request, 'role/role_form.html', locals())

@permission_check(['r_role'])
def RoleSearchView(request):
    ''' role search '''
    search_filter = request.GET.get('search_filter', '')
    q = Q(name__icontains=search_filter) | Q(users__username__icontains=search_filter)
    roles = Role.objects.select_related().filter(q).distinct()
    return render(request, 'role/role_list.html', locals())

@permission_check(['u_role'])
def DeleteUserFromRole(request, rid='', uid=''):
    ''' remove user from role '''
    try:
        role = Role.objects.get(pk=rid)
        role.users.remove(uid)
        res = {'code': 1, 'msg': '该用户已从用户组删除'}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    return JsonResponse(res)

@permission_check(['u_role'])
def RoleUpdateView(request, pk=''):
    ''' RoleUpdate '''
    users = User.objects.all()
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        try:
            role.name = request.POST.get('name', '')
            role.save()
            role.users = request.POST.getlist('users[]', '')
            res = {'code': 1, 'msg': '角色已经更新！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    return render(request, 'role/role_update.html', locals())

@permission_check(['d_role'])
def RoleDeleteView(request, pk=''):
    ''' GroupDelete '''
    try:
        Role.objects.filter(pk=pk).delete()
        res = {'code': 1, 'msg': '删除成功 ！'}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    return JsonResponse(res)

@permission_check(['r_perm'])
def PermListView(request):
    ''' permssion list'''

    # 查询处理
    search_filter = request.GET.get('search_filter', '')
    role_selected = request.GET.get('role', '')
    q = Q(module__icontains=search_filter) | Q(name__icontains=search_filter)

    perms = Perm.objects.select_related().filter(q).distinct().order_by('id')
    roles = Role.objects.order_by('id')

    # 构造返回数据结构
    if role_selected:
        all_role = Role.objects.filter(pk=role_selected)
        role_selected = all_role[0]
    else:
        all_role = roles

    perm_list = []
    for perm in perms:
        row = {'perm_id': perm.id, 'perm_module': perm.module, 'perm_name': perm.name}
        role_list = []
        for role in all_role:
            if role in perm.role_set.all():
                role_list.append(role.id)
            else:
                role_list.append(0)
        row['roles'] = role_list
        perm_list.append(row)
    
    return render(request, 'permission/permission_list.html', locals())

@permission_check(['u_perm'])
def PermUpdateView(request):
    ''' permssion update'''
    if request.method == 'POST':
        try:
            # querydict转换成字典
            post_data = request.POST.dict()

            del post_data['csrfmiddlewaretoken']

            # 一个权限对应多个角色
            from collections import defaultdict
            d = defaultdict(list)
            for item in post_data.keys():
                perm_id, role_id = item.split('-')
                d[perm_id].append(int(role_id))

            # 给权限添加角色
            for perm, roles in d.iteritems():
                perm_obj = Perm.objects.get(pk = perm)
                perm_obj.role_set = roles

            res = {'code': 1, 'msg': '保存成功 ！'}
        except Exception as e:
            res = {'code': 1, 'msg': str(e)}
        return JsonResponse(res)

    # 查询处理
    perms = Perm.objects.order_by('id')
    all_role = Role.objects.order_by('id')

    # 构造返回数据结构
    perm_list = []
    for perm in perms:
        row = {'perm_id': perm.id, 'perm_module': perm.module, 'perm_name': perm.name}
        role_list = []
        for role in all_role:
            if role in perm.role_set.all():
                role_list.append({'status': True, 'id': role.id})
            else:
                role_list.append({'status': False, 'id': role.id})
        row['roles'] = role_list
        perm_list.append(row)
    
    return render(request, 'permission/permission_update.html', locals())

@permission_check(['r_service'])
def ServiceListView(request):
    ''' system service list view '''
    services = Service.objects.all()
    return render(request, 'service/service_list.html', locals())

@permission_check(['u_service'])
def ServiceUpdateView(request, pk=''):
    ''' system service update view '''
    if request.method == 'POST':
        try:
            post_data = { key: value for key, value in request.POST.iteritems() if key != 'csrfmiddlewaretoken' }
            print post_data
            Service.objects.filter(pk=pk).update(**post_data)
            res = {'code': 1, 'msg': '服务配置已经更新！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'service/service_update.html', locals())