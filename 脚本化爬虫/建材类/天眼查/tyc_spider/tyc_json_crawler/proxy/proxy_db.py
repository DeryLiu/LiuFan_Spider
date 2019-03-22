# -*- coding:utf-8 -*-
from proxy_url import parserList as e
from lxml import etree
import requests
from mysql_db import Mysql_DB
import sys
from proxy_test import test_proxy
reload(sys)
from multiprocessing import Process

sys.setdefaultencoding('utf8')


headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}



def liuliu_proxy(i):
    urls = e[i]["urls"]
    for url in urls:
        try:
            db = Mysql_DB()
            response = requests.get(url,headers=headers)
            html = etree.HTML(response.text)
            ip_list = html.xpath(e[i]["pattern"]+e[i]["position"]["ip"])
            port_list = html.xpath(e[i]["pattern"]+e[i]["position"]["port"])
            type_list = html.xpath(e[i]["pattern"]+e[i]["position"]["type"])
        except Exception as h:
            print(u'异常%s'%h)
        else:
            for m in range(len(ip_list)):
                ip = ip_list[m].text.encode('utf-8').strip()
                port = port_list[m].text.encode('utf-8').strip()
                tp = type_list[m].text.encode('utf-8').strip()
                if test_proxy(ip,port):
                    print(url+u'代理好使%s'%ip)
                    db.put('proxy_db',ip,port,tp)
                else:
                    print(url+u'无效代理%s' %ip)
        finally:
            db.close()


if __name__ =='__main__':
    for i in range(5):
        p = Process(target=liuliu_proxy, args=(i,))
        p.start()

    #liuliu_proxy()