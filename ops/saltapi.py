# -*- coding: utf-8 -*-
###
# author: wei.yang@jinmuinfo.com
###
import requests
import json


class SaltAPI():
    def __init__(self, host, username, password, port=443, auth="pam"):
        self.host = host
        self.port = port
        self.username = username
        self.passoword = password
        self.auth = auth
        self.headers = {
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        self.post_data = ""
        self.headers['X-Auth-Token'] = self.login()

    def do_post(self, api=""):
        url = "https://%s:%s/%s" % (self.host, self.port, api)
        post_req = requests.post(url,data=json.dumps(self.post_data),headers=self.headers,verify=False)
        return post_req.json()["return"][0]

    def login(self):
        self.post_data = {
            "username": self.username,
            "password": self.passoword,
            "eauth": self.auth
        }
        url = "https://%s:%s/%s" % (self.host, self.port, 'login')
        post_req = requests.post(url,data=json.dumps(self.post_data),headers=self.headers,verify=False)
        resp = post_req.json()["return"][0]
        # self.headers['X-Auth-Token'] = resp["token"]
        return resp["token"]

    def run(self, client='local', fun="test.ping", target="*", arg_list=[],expr_form='list'):
        self.post_data = [
            {
                "client": client,
                "tgt": target,
                "fun": fun,
                "expr_form": expr_form,
                "arg": arg_list
            }
        ]
        return self.do_post()

    def run_async(self, client='local_async', fun="test.ping", target="*", arg_list=[],expr_form='list'):
        self.post_data = [
            {
                "client": client,
                "fun": fun,
                "tgt": target,
                "expr_form": expr_form,
                "arg": arg_list
            }
        ]
        return self.do_post()


    def key(self, client='wheel', fun="key.accept", match=[]):
        if match:
            self.post_data = [
                {
                    "client": client,
                    "fun": fun,
                    "match": match
                }
            ]
        else:
            self.post_data = [
                {
                    "client": client,
                    "fun": fun
                }
            ]
        return self.do_post()

    def minion_alive_check(self, client='runner', fun="manage.down", target="*"):
        self.post_data = [
            {
                "client": client,
                "tgt": target,
                "fun": fun
            }
        ]
        return self.do_post()

