# -*- coding: UTF-8 -*-
'''
Python 3.x
无忧代理IP Created on 2018年07月11日
描述：本段代码定时从无忧代理API接口获取代理IP，存入IP池中
@author: www.data5u.com
'''
import requests
import time
import threading
from data5u import IPPOOL
from requests.packages import urllib3

# 获取代理IP的线程类
class GetIpThread(threading.Thread):
    def __init__(self,apiUrl, fetchSecond):
        super(GetIpThread, self).__init__()
        self.fetchSecond=fetchSecond
        self.apiUrl=apiUrl
    def run(self):
        while True:
            # 获取IP列表
            res = requests.get(self.apiUrl).content.decode()
            # 按照\n分割获取到的IP
            IPPOOL = res.split('\n')
            # 休眠
            time.sleep(self.fetchSecond)