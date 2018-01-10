#!/usr/bin/python
#coding=utf-8

'''
author: wei.yang@jinmuinfo.com
date: 2017.07.28

function:
cronjob for app ops

requirements:
'''

from .saltapi import SaltAPI
from devops.settings import SALT_IP, SALT_PORT, SALT_USER, SALT_PASSWD
from devops.settings import mongo

def check_minion_status(arg, arg1, target, arg_list):
  '''
  monitoring host salt-minion status
  '''
  try:
    salt = SaltAPI(SALT_IP,SALT_USER,SALT_PASSWD,port=SALT_PORT)
    ret = salt.minion_alive_check()
    mongo.devops.host.update_many({'minion_status': 'error'}, {'$set': {'minion_status': 'ok'}})
    if ret:
      for minion in ret:
        try:
          mongo.devops.host.update({'minion_id': minion}, {'$set': {'minion_status': 'error'}})
        except Exception as e:
          # continue
          print str(e)
  except Exception as e:
    print str(e)

def update_grains(arg, arg1, target, arg_list):
  '''
  update all hosts grains in a interval
  '''
  try:
    salt = SaltAPI(SALT_IP, SALT_USER, SALT_PASSWD, port=SALT_PORT)
    salt.run(client='local_async', fun="grains.items", target="*", arg_list=['--batch=10%'], expr_form='glob')
  except Exception as e:
    print str(e)


