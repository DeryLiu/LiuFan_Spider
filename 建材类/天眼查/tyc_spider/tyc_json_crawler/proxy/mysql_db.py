# -*- coding:utf-8 -*-

import pymysql

class Mysql_DB(object):
    def __init__(self,host='127.0.0.1',user='root',password='123',db='db',port=3306,charset='utf8'):
        self.host=host
        self.user=user
        self.password=password
        self.db=db
        self.port=port
        self.charset=charset

        self.conn = pymysql.connect(host=self.host,user=self.user,password=self.password,db=self.db,port=self.port,charset=self.charset)
        self.cur = self.conn.cursor()
        #except Exception as e:
         #   print(u'链接数据库异常%s'%e)


    def put(self,table,ip,port,type):
        sql='INSERT INTO '+table+' (ip,port,type)VALUES(%s,%s,%s)'
        self.cur.execute(sql,(ip,port,type))
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()