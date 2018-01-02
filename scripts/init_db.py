# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from admins.models import Role, Perm, Service

# create permission
# c(create): 新建, r(retrieve): 查询, u(update): 更新, d:(delete): 删除 
perms_list = [
    {
        '用户管理':
            [
                {'name': '新建用户', 'code': 'c_user'},
                {'name': '查询用户', 'code': 'r_user'},
                {'name': '更新用户', 'code': 'u_user'},
                {'name': '删除用户', 'code': 'd_user'}
            ],
        '用户组管理':
            [
                {'name': '新建用户组', 'code': 'c_user_group'},
                {'name': '查询用户组', 'code': 'r_user_group'},
                {'name': '更新用户组', 'code': 'u_user_group'},
                {'name': '删除用户组', 'code': 'd_user_group'}
            ]
    },
    {
        '权限列表':
            [
                {'name': '查询权限', 'code': 'r_perm'},
                {'name': '更新权限', 'code': 'u_perm'}
            ],
        '角色管理':
            [
                {'name': '新建角色', 'code': 'c_role'},
                {'name': '查询角色', 'code': 'r_role'},
                {'name': '更新角色', 'code': 'u_role'},
                {'name': '删除角色', 'code': 'd_role'}
            ]
    },
    {
        '服务管理':
            [
                {'name': '查询服务', 'code': 'r_service'},
                {'name': '更新服务', 'code': 'u_service'}
            ]
    },
    {
        '资源模型':
            [
                {'name': '新建模型', 'code': 'c_model'},
                {'name': '查询模型', 'code': 'r_model'},
                {'name': '更新模型', 'code': 'u_model'},
                {'name': '删除模型', 'code': 'd_model'},
                {'name': '新建属性', 'code': 'c_field'},
                {'name': '查询属性', 'code': 'r_field'},
                {'name': '更新属性', 'code': 'u_field'},
                {'name': '删除属性', 'code': 'd_field'}
            ],
        '主机管理':
            [
                {'name': '添加主机', 'code': 'c_host'},
                {'name': '查询主机', 'code': 'r_host'},
                {'name': '更新主机', 'code': 'u_host'},
                {'name': '删除主机', 'code': 'd_host'},
                {'name': '导入主机', 'code': 'import_host'},
                {'name': '导出主机', 'code': 'export_host'}
            ]
    },
    {
        '作业平台':
            [
                {'name': '命令执行', 'code': 'run_cmd'},
                {'name': '文件传输', 'code': 'push_file'},
                {'name': '上传文件', 'code': 'upload_file'},
                {'name': '删除文件', 'code': 'delete_file'},
                {'name': '执行脚本', 'code': 'run_script'},
                {'name': '执行模块', 'code': 'run_state'}
            ]
    }
]

for item in perms_list:
    try:
        for module, perms in item.iteritems():
            for perm in perms:
                permission, status = Perm.objects.update_or_create(module=module, name=perm['name'], code=perm['code'])
                print '%s -- %s -- %s'%(module, perm['name'], perm['code'])
    except Exception as e:
        print str(e), 'create permission'
        continue

# create roles
role_list = ['管理员', '运维', '测试', '开发', '普通用户']
for name in role_list:
    try:
        role, role_created = Role.objects.get_or_create(name=name)
        if role_created:
            print '******************', '创建角色: %s'%(name), '******************'
        if role:
            if role.name.encode('utf-8') == '管理员':
                perms = Perm.objects.all()
                role.perms = [ perm.id for perm in perms ]
    except Exception as e:
        print str(e),'create roles' 
        continue

# create user group
user_group_list = ['管理员']
for group_name in user_group_list:
    try:
        group, group_created = Group.objects.get_or_create(name=group_name)
        if group_created:
            print '******************', '创建用户组: %s'%(group_name), '******************'
    except Exception as e:
        print str(e), 'create user group'
        continue

# create admin user
admin_user_list = [{'username': 'admin', 'password': 'admin@123'}]
try:
    for user in admin_user_list:
        user_instance, created = User.objects.get_or_create(username=user['username'], defaults={'is_superuser': True})
        if created:
            user_instance.set_password(user['password'])
            user_instance.save()
            print '******************', '创建用户: %s'%(user_instance.username), '******************'
        if user_instance:
            role, role_created = Role.objects.get_or_create(name='管理员')
            if role:
                role.users.add(user_instance)
                print '******************', '赋予%s用户 %s 角色'%(user_instance.username.encode('utf-8'), \
                role.name.encode('utf-8')), '******************'
            group, group_created = Group.objects.get_or_create(name='管理员')
            if group:
                user_instance.groups.add(group)
                print '******************', '分配%s用户到 %s 用户组'%(user_instance.username.encode('utf-8'), \
                group.name.encode('utf-8')), '******************'
except Exception as e:
    print str(e)

# create service for devops
service_list = [
    # {
    # 'name': 'salt_master_server',
    # 'host': '0.0.0.0',
    # 'port': 22,
    # 'comment': 'saltstack master所在机器,提供文件分发等服务'
    # },
    # {
    # 'name': 'salt_api',
    # 'host': '0.0.0.0',
    # 'port': 8080,
    # 'comment': '作业平台基于saltstack API开发'
    # },
    # {
    # 'name': 'mongodb',
    # 'host': '0.0.0.0',
    # 'port': 27017,
    # 'comment': '存储资产数据'
    # },
    # {
    # 'name': 'zabbix',
    # 'host': '0.0.0.0',
    # 'port': 80,
    # 'comment': 'zabbix监控'
    # },
    {
    'name': 'webssh',
    'host': '0.0.0.0',
    'port': 9527,
    'comment': 'web终端服务'
    },
    {
    'name': 'ftp',
    'host': '0.0.0.0',
    'port': 80,
    'comment': '文件服务器'
    }
]
for service in service_list:
    try:
        Service.objects.get_or_create(name=service['name'], defaults={'host': service['host'], 'port': service['port'], 'comment': service['comment']})
        print '*'*20, '新建或更新系统服务：%s'%(service['name']), '*'*20
    except Exception as e:
        print str(e)
        break

# create configration category
from cmdb.models import CiCategory, CiProperty
ci_c_list = [
    {
        'name': '主机管理',
        'code': 'host', 
        'show_in_left': True, 
        'comment': '主机管理', 
        'is_must': True,
        'properties':[
                {
                    'name': '服务器ID', 
                    'code': 'server_id', 
                    'is_must': True, 
                    'is_edit': False,
                    'form_type': 'required', 
                    'value_type': 'str', 
                    'show_in_table': False, 
                    'is_search': False
                },
                {
                    'name': '主机名', 
                    'code': 'hostname', 
                    'is_must': True, 
                    'is_edit': False,
                    'form_type': 'required', 
                    'value_type': 'str', 
                    'show_in_table': True, 
                    'is_search': True
                },
                {
                    'name': 'IP地址', 
                    'code': 'ip', 
                    'is_must': True, 
                    'is_edit': False,
                    'form_type': 'required', 
                    'value_type': 'str', 
                    'show_in_table': True, 
                    'is_search': True
                },
                {
                    'name': '操作系统', 
                    'code': 'os', 
                    'is_must': True, 
                    'is_edit': False,
                    'form_type': 'required', 
                    'value_type': 'str', 
                    'show_in_table': True, 
                    'is_search': True
                },
                {
                    'name': 'CPU', 
                    'code': 'cpu', 
                    'is_must': True, 
                    'is_edit': False,
                    'form_type': 'required', 
                    'value_type': 'str', 
                    'show_in_table': True, 
                    'is_search': True
                },
                {
                    'name': '内存 (G)', 
                    'code': 'memSize', 
                    'is_must': True, 
                    'is_edit': False,
                    'form_type': 'required', 
                    'value_type': 'str', 
                    'show_in_table': True, 
                    'is_search': True
                },
                {
                    'name': '虚拟/物理', 
                    'code': 'is_virtual', 
                    'is_must': True, 
                    'is_edit': False,
                    'form_type': 'required', 
                    'value_type': 'str', 
                    'show_in_table': True, 
                    'is_search': True
                },
                {
                    'name': '网卡', 
                    'code': 'eth', 
                    'is_must': True, 
                    'is_edit': False,
                    'form_type': 'required', 
                    'value_type': 'str', 
                    'show_in_table': True, 
                    'is_search': False
                },
                {
                    'name': '硬盘', 
                    'code': 'disk', 
                    'is_must': True, 
                    'is_edit': False,
                    'form_type': 'required', 
                    'value_type': 'str', 
                    'show_in_table': False,
                    'is_search': False
                },
                {
                    'name': 'Salt客户端ID', 
                    'code': 'minion_id', 
                    'is_must': True, 
                    'is_edit': False,
                    'form_type': 'optional', 
                    'value_type': 'str', 
                    'show_in_table': True, 
                    'is_search': False
                },
                {
                    'name': 'Salt客户端状态', 
                    'code': 'minion_status', 
                    'is_must': True, 
                    'is_edit': False,
                    'form_type': 'optional', 
                    'value_type': 'str', 
                    'show_in_table': True, 
                    'is_search': True
                },
                {
                    'name': '运营状态', 
                    'code': 'host_status', 
                    'is_must': True, 
                    'form_type': 'required', 
                    'value_type': 'str', 
                    'show_in_table': True, 
                    'is_search': True, 
                    'optional_value': '运营中;故障中;未上线;下线隔离中;开发机;测试机;维修中;报废'
                },
                {
                    'name': '运维负责人', 
                    'code': 'admin', 
                    'is_must': True, 
                    'form_type': 'required', 
                    'value_type': 'array', 
                    'show_in_table': True, 
                    'is_search': True
                },
                {
                    'name': '标签', 
                    'code': 'tags', 
                    'is_must': True, 
                    'form_type': 'optional', 
                    'value_type': 'array', 
                    'show_in_table': True, 
                    'is_search': True
                },
                {
                    'name': '环境', 
                    'code': 'env', 
                    'is_must': True, 
                    'form_type': 'required', 
                    'value_type': 'str', 
                    'show_in_table': True, 
                    'is_search': True, 
                    'optional_value': '开发;测试;生产'
                }
        ]
    }
]
for category in ci_c_list:
    try:
        obj, status = CiCategory.objects.update_or_create(name=category['name'], code=category['code'], \
        defaults={'show_in_left': category['show_in_left'], 'comment': category['comment'], \
        'is_must': category['is_must']})
        if status:
            print '*'*20, '新建资源模型：%s'%(obj.name), '*'*20
        if obj:
            for item in category['properties']:
                property_obj, is_created = CiProperty.objects.update_or_create(name=item['name'], \
                code=item['code'], ci_category_id=obj.id, defaults={'is_must':item['is_must'], 'form_type': item['form_type'], \
                'value_type': item['value_type'], 'show_in_table': item['show_in_table']})
                if 'optional_value' in item.keys():
                    property_obj.optional_value = item['optional_value']
                if 'is_edit' in item.keys():
                    property_obj.is_edit = item['is_edit']
                property_obj.save()
                print '配置项分类:%s ---- 配置项属性:%s'%(property_obj.ci_category.name.encode('utf-8'), property_obj.name.encode('utf-8'))
    except Exception as e:
        raise e
        # print str(e)
        # break


from devops.settings import scheduler
from ops.jobs import check_minion_status,update_grains
try:
    job1 = scheduler.cron('*/10 * * * *',func=check_minion_status,args=['','',['all'],'checking minions status'],repeat=None,queue_name='default')
    print job1
    job2 = scheduler.cron('0 0 */3 * *',func=update_grains,args=['','',['all'],'updating grains'],repeat=None,queue_name='default')
    print job2
except Exception as e:
    print e
