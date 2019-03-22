# -*- coding:utf-8 -*-

import requests

url = 'http://www.baidu.com'

def test_proxy(ip,port):
    ip = str(ip)
    port = str(port)
    IP = 'http://'+ip+':'+port
    proxy = {'http':IP}
    NETWORK_STATUS = True

    try:
        requests.get(url, proxies=proxy, timeout=3)
    except:
        NETWORK_STATUS = False

    return NETWORK_STATUS
