# -*- coding:utf-8 -*-
'''
5月5日 增加提交表单（基本信息），及判断内容，state==ok则正确返回信息，否则error
同时加入自定义requests(代理IP， 头文件)
'''
#import requests
from Download import request
import pymysql
import json
from urllib import quote
from Comp_Lists import url_list,infs_list
from multiprocessing import Process,Lock,Queue
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#proxy = {"http":"http://185.128.36.100:8080"}

def main_tyc(queues,lock):

    def get_main(na,id):
        number = str(id)
        name = str(na)
        urls = get_url(name, number)
        print len(urls)
        datas = map(get_com, urls)
        # 实例化每个父项目内容
        data1 = get_data(0, 12, datas)
        data2 = get_data(12, 18, datas)
        data3 = get_data(18, 23, datas)
        data4 = get_data(23, 27, datas)
        data5 = get_data(27, 33, datas)
        data6 = get_data(33, 40, datas)
        data7 = get_data(40, 44, datas)
        # 存储到数据库
        put_db(name, data1, data2, data3, data4, data5, data6, data7)

#将获取的子项目内容归档到父项目中，并返回json形式
    def get_data(a,b,datas):
        data_dict = {}
        for i in range(a,b):
            data_dict[infs_list[i]] = datas[i]
        data_js = json.dumps(data_dict, ensure_ascii=False)
        return data_js

    #解析url返回的json，获取其中的data
    def get_com(url):
        response = request.get(url)
        try:
            dict_url = json.loads(response.text)
            print response.status_code, url
        except:
            print(u'异常:%s'%url)
            #data='iperror'
            request.proxies.pop(0)
            print(u'换个代理继续加载')
            return get_com(url)
        else:
            #返回正确数据
            if dict_url["state"] == "ok":
                try:
                    data = dict_url["data"]
                except:
                    data = dict_url["courtAnnouncements"]
                #有可能为空数据
                finally:
                    data = json.dumps(data, ensure_ascii=False)
                    return data
            #返回数据错误
            elif dict_url["state"] == "error":
                data = "error"
                return data
            elif dict_url["state"] == "warn":
                data = "warn"
                return data
            else:
                data = "dataerror"
                return data

    #通过公司名字和id获取对应内容的url
    def get_url(name,number):
        urls = []
        uname = quote(name)
        unumber = str(number)
        number_urls = range(18, 26)+ range(28, 32) + [34, 35, 37]
        for i in range(44):
            if i in number_urls:
                url = url_list[i] %uname
            else:
                url = url_list[i] %unumber
            urls.append(url)
        return urls

    # 将信息存入数据库
    def put_db(name, data1, data2, data3, data4, data5, data6, data7):
        name = str(name)
        try:
            conn = pymysql.connect(host='127.0.0.1', user='root', password='123', db='tyc', port=3306, charset='utf8')
            cur = conn.cursor()
            sql = 'INSERT INTO tyc_10_6 (name,ssxx,qybj,qyfz,sffx,jyfx,jyzk,zscq)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
            cur.execute(sql, (name, data1, data2, data3, data4, data5, data6, data7))
            conn.commit()
            print(u'%s导入成功' % name)
        except Exception as e:
            print(u'导入异常%s' % e)
            print(u'失败%s' % name)
        finally:
            cur.close()
            conn.close()

    #获取公司名字和id
    def get_name_id():
        while not queues.empty():
            lock.acquire()
            try:
                com = queues.get()
                name = com[0]
                number = com[1]

            finally:
                lock.release()
                if len(number) == 0:
                    print(name+u'不存在')
                    pass
                else:
                    get_main(name,number)

    get_name_id()


if __name__=="__main__":
    coms = Queue()
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123', db='test15', port=3306, charset='utf8')
    cur = conn.cursor()
    sql = 'SELECT name,number FROM tyc_10_c1 LIMIT 3164,1000'
    cur.execute(sql)
    conn.commit()
    comps = cur.fetchall()
    cur.close()
    conn.close()
    for com in comps:
        coms.put(com)
    lock = Lock()


    processes = []
    for i in range(8):
        p = Process(target = main_tyc, args=(coms,lock))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()

    #main_tyc(coms,lock)
    print(u'爬取完成')

