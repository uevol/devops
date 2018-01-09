# -*- coding: utf-8 -*-
###
# author: wei.yang@jinmuinfo.com
# date : 2017-10-23
from pyzabbix import ZabbixAPI
from devops.settings import ZABBIX_SERVER, ZABBIX_PORT, ZABBIX_PATH, ZABBIX_USER, ZABBIX_PASS
import datetime
import time

try:
	if ZABBIX_PORT:
		ZABBIX_URL = "http://" + ZABBIX_SERVER + ":" + str(ZABBIX_PORT) + ZABBIX_PATH
	else:
		ZABBIX_URL = "http://" + ZABBIX_SERVER + ZABBIX_PATH
	zapi = ZabbixAPI(ZABBIX_URL)
	zapi.login(ZABBIX_USER,ZABBIX_PASS)
except Exception as e:
	print "zabbix api error: %s"% (str(e))

def get_hostid_by_ip(ip):
	data, error = '', ''
	try:
		data = zapi.hostinterface.get(output=['hostid'],filter={'ip':ip})
		if data:
			data = data[0]['hostid']
	except Exception as e:
		error = str(e)
	return data, error

def get_itemids_by_hostid(hostid,key):
	ret, error = {}, ''
	try:
		data = zapi.item.get(output=['itemid','key_'],hostids=hostid,search={"key_": key})
		if data:
			for ele in data:
				ret[ele['key_']] = ele['itemid']
	except Exception as e:
		error = str(e)

	return ret, error


def get_graph_by_ip(ip):
	ret, error = {}, ''
	try:
		hostid, error = get_hostid_by_ip(ip)
		if not error:
			graphids = zapi.graph.get(output=["graphid",'name'],hostids=hostid)
			if graphids:
				for ele in graphids:
					ret[ele['name']] = ele['graphid']
	except Exception as e:
		error = str(e)
	return ret, error

def get_item_by_graphid(graphid):
	ret, error = {}, ''
	try:
		itemids = zapi.graphitem.get(output=['itemid'],graphids=graphid)
		if itemids:
			ids = []
			for ele in itemids:
				ids.append(ele['itemid'])
			items = zapi.item.get(output=['key_'],itemids=ids)
			if items:
				for ele in items:
					ret[ele['key_']] = ele['itemid']
	except Exception as e:
		error = str(e)
	return ret, error

def get_history_data(itemids=[],time_from=time.time() - 60 * 60 * 1,time_till=time.time()):
	try:
		history, error = {}, ''
		# Query item's history (integer) data
		history = zapi.history.get(itemids=itemids,
								   time_from=time_from,
								   time_till=time_till,
								   output='extend',
								   sortfield="clock",
								   sortorder="ASC",
								   )

		# If nothing was found, try getting it from history (float) data
		if not len(history):
			history = zapi.history.get(itemids=itemids,
									   time_from=time_from,
									   time_till=time_till,
									   output='extend',
									   sortfield="clock",
									   sortorder="ASC",
									   history=0
									   )
	except Exception as e:
		error = str(e)
	
	return history, error
