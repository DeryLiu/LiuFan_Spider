import requests
import re
from io import StringIO
import gzip
from distutils.log import info
import os
from multiprocessing import Pool,Lock
import logging
import logging.config
from Tools import get_html,ALL_CONFIG

import select
import config

logging.config.fileConfig("./log/logging.conf")    # 采用配置文件  
logger1 = logging.getLogger("logger1")   
logger2 = logging.getLogger("logger2") 

'''
    获取网页的源代码
'''
# def get_html(url):
#     try:
#         headers = {
#                     "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0",
#                     "Content-Type":"text/html; charset=UTF-8",
#                     "Content-Encoding":"gzip",
#                             }
#         req = urllib2.Request(url, None, headers)
#         response = urllib2.urlopen(req, timeout=10)
#         html = response.read()
#         gzipped = response.headers.get('Content-Encoding','')
#         if gzipped:
#             compressedstream = StringIO.StringIO(html)
#             gzipper = gzip.GzipFile(fileobj=compressedstream)
#             data = gzipper.read()
#             html = data
#         return html
#     except Exception as e:
#         print 'error:', str(e)
#         logger2.error(str(e))
#         get_html(url)
'''
    获取书籍页面
'''
def get_book_html(line):
    print ('---------------------get_book_html begin----------------------')
    url=line.replace('\n','')
    book_id=re.findall('http://product.half.ebay.com/.*?/(.*?)&.*?tg=info',url)[0]
    html = get_html.get_html(url)
    if html:
        with open('./result/'+opt[0]+'/book/' + book_id + '.html','w') as ff:
                ff.write(html)
        print ('success:',url)
    else:
        with open('./result/'+opt[0]+'/get_book_html_fail.txt','aw') as fff:
            fff.write(line)
        with open('./result/'+opt[0]+'/get_book_info_fail.txt','aw') as ffff:
            ffff.write(line.replace('\n','')+'.html' + '\n')
        print ('fail:',url)
    print ('---------------------get_book_html end----------------------')

'''
    获取书籍页面
'''
if __name__ == '__main__':
    global opt
    opt=config.opt.split('|')
    logger1.info(opt[0]+'get book html begin')
    if os.path.exists('./result/'+opt[0]+'/book')==0:
        os.mkdir('./result/'+opt[0]+'/book')
    with open('./result/'+opt[0]+'/book_url.txt') as r:
        lines = r.readlines()
    begin=config.begin_num
    end=config.end_num
    if begin!='' and end!='':
        lines=lines[int(begin):int(end)]
    elif begin!='':
        lines=lines[int(begin):]
    elif end!='':
        lines=lines[:int(end)]
    pool = Pool(3)
    pool.map(get_book_html,lines)
    pool.close()
    pool.join()

    os.system('nohup python get_book_info.py &')
    logger1.info(opt[0]+'get book html end')
