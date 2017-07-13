import random
import requests
import re
from io import StringIO
import gzip
import os
from multiprocessing import Pool,Lock
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import time
import logging
import logging.config

def send_asin_email(file):
    #创建一个带附件的实例
    msg = MIMEMultipart()
    #构造附件1
    att1 = MIMEText(open('./info/onshelf_info.csv', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="success_asin.txt"'#这里的filename可以任意写，写什么名字，邮件中显示什么名字
    msg.attach(att1)
    #加邮件头
    #to_list=['liz0505@starmerx.com','lujuan@starmerx.com','lily@starmerx.com','jiping@starmerx.com']#发送给相关人员
    #     to_list=['3394722605@qq.com','miaomiao@starmerx.com','zhaolei@starmerx.com']
    to_list=['user']
    msg['to'] = ';'.join(to_list)
    msg['from'] = 'user'
    msg['subject'] = 'half新数据'
    #发送邮件
    try:
        server = smtplib.SMTP()
        server.connect('smtp.exmail.qq.com')
        server.login('user','pwd')#XXX为用户名，XXXXX为密码
        server.sendmail(msg['from'], to_list,msg.as_string())
        print ('发送成功','./info/onshelf_info.csv')
    except Exception as e:
        print ('发送失败',e)
        #server.quit()
        send_asin_email('./info/onshelf_info.csv')
    finally:
        server.quit()

if __name__ == '__main__':
    file = ''
    send_asin_email(file)