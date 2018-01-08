#!/usr/bin/python
#coding=utf-8
'''
author: wei.yang@jinmuinfo.com
date: 2017.12.15

function:
Listening Salt Master Event System and parase the job return ,then post result to devops
'''
import json

# set logger
try:
    import logging
    logging.basicConfig(level=logging.ERROR,
                        format="%(asctime)s %(name)s %(levelname)s %(lineno)s -- %(message)s",
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='error.log')
    logger = logging.getLogger('forward_to_devops')
except Exception as e:
    raise e

# For Python 2 and 3 compatibility
try:
    import urllib2
except ImportError:
    # Since Python 3, urllib2.Request and urlopen were moved to
    # the urllib.request.
    import urllib.request as urllib2

def post_data_to_devops(data, url="http://devops:9000/cmdb/host/createOrUpdate/"):
    ''' post data to devops '''
    data = json.dumps(data)
    if isinstance(data, bytes):
        data = data.encode('utf-8')

    req = urllib2.Request(url, data)
    req.add_header('Content-Type', 'application/json')

    try:
        res = urllib2.urlopen(req)
        res_str = res.read().decode('utf-8')
        # print type(res.read()), res_str
        # res_json = json.loads(res_str)
        if "error" in res_str:
            logger.error(str(res_str))
    except Exception as e:
        # loggin error
        logger.error(str(e))

# import salt-api lib
try:
    import salt.config
    import salt.utils.event
except Exception as e:
    logger.error(str(e))
    raise e

# Listen Salt Master Event System
try:
    # print '+'*20, 'Starting to listen salt master event system', '+'*20
    __opts__ = salt.config.client_config('/etc/salt/master')
    event = salt.utils.event.MasterEvent(__opts__['sock_dir'])

    # create re pattern objects according to event type
    import re
    pattern_job_ret = re.compile(r'salt/job/\d+/ret/.+')

    # iter salt event
    for eachevent in event.iter_events(full=True):
        try:
            if pattern_job_ret.match(eachevent['tag']):
                if eachevent['data'].has_key('id') and eachevent['data'].has_key('return'):
                    data = {}
                    if eachevent['data']['fun'] == 'grains.items':
                        items = eachevent['data']['return']
                        # keys = ['server_id', hostname', 'ip', 'os', 'cpu', 'memSize', 'is_virtual', 'eth', 'disk']
                        data['server_id'] = str(items['server_id'])
                        data['hostname'] = items['nodename']
                        data['ip'] = [ ip for ip in items['ipv4'] if ip != '127.0.0.1'][0]
                        data['os'] = ' '.join([items['os'], items['osrelease']])
                        data['cpu'] = ' * '.join([str(items['num_cpus']), items['cpu_model']])
                        data['memSize'] = items['mem_total'] / 1024 + 1
                        data['is_virtual'] = items.get('virtual', '')
                        data['eth'] = str(items['hwaddr_interfaces'])
                        data['minion_id'] = items['id']
                        data['minion_status'] = 'ok'
                        data['category'] = 'host'
                        data['api_type'] = 'host_garins'
                    elif eachevent['data']['fun'] == 'disk.usage':
                        data['minion_id'] = eachevent['data']['id']
                        data['disk'] = eachevent['data']['return']
                        data['api_type'] = 'host_disk'
                    elif eachevent['data']['fun'] == 'state.sls':
                        ret = eachevent['data']['return']
                        tmp = {'process':{},'summary':{}}
                        succeeded = 0
                        failed = 0
                        total_duration = 0
                        for k,v in ret.items():
                            tmp1 = k.split('_|-')
                            fun = '.'.join([tmp1[0],tmp1[3]])
                            v['fun'] = fun
                            v['id'] = tmp1[1]
                            tmp['process'].update({str(v['__run_num__']):v})
                            if v['result'] == True:
                                succeeded += 1
                            else:
                                failed += 1
                            total_duration += v['duration']
                        tmp['summary'].update({'succeeded':succeeded,'failed':failed,'total_duration':total_duration})
                        eachevent['data']['return'] = str(tmp)
                        data = eachevent['data']
                    else:
                        continue
                    post_data_to_devops(data)
                    # the following code is for debugging
                    # import pprint
                    # pprint.pprint(data)

        except Exception as e:
            # loggin error
            logger.error(str(e))
            continue
except Exception as e:
    raise e
