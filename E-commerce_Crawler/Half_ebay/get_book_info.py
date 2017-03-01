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

def create_titles(filename,titles):
    f = open(filename,"w")
    f.write("\t".join(titles)+"\n")
    f.flush()
    f.close()

'''
    解析书籍详细信息
''' 
def get_book_info(filename):
    print ('---------------------get_book_info begin----------------------')
    book_id_url = {}
    with open('./result/'+opt[0]+'/book_url.txt') as uu:
        lines = uu.readlines()    
    for line in lines:
        url = line.replace('\n','')
        book_id = re.findall('http://product.half.ebay.com/.*?/(.*?)&.*?tg=info',url)[0]
        book_id_url[book_id] = url

    books_id = filename.split('.')[0]
    if not book_id.isspace():
        book_url =book_id_url[books_id] 
        with open('./result/'+opt[0]+'/book/' + filename) as f:
            html = f.read()
        with open('./result/'+opt[0]+'/book_info.txt','aw') as ff:
            try:
                isbn=''
                isbn13=''
                condition=[]
                weight=''
                book_format=''
                language=''
                publisher='' 
                author=''
                publish_time=''
                details=[]
                title=''
                title=re.findall('<h1 class="pdppagetitle">(.*?)</h1>',html)[0]
                time=re.search('(\d+),(\D+)',title)
                if time:
                    publish_time=time.group(1)
                #print publish_time 
                au=re.findall('Author: <span class="pdplinks"><a href=.*? class="pdplinks">(.*?)</a>',html)
                if au:
                    author=au[0]
                myformat=re.findall('Format:</b> <span .*?>(.*?)</span>',html)
                if myformat:
                    book_format=myformat[0]
                isbn=re.findall('ISBN-10:</b>\s+<span class=""><a href=.*? class="pdplinks">(.*?)</a>',html)[0]
                isbn_13=re.findall('ISBN-13:</b>\s+<span class=""><a href=.*? class="pdplinks">(.*?)</a>',html)
                if isbn_13:
                    isbn13=isbn_13[0]
                puber=re.findall('Publisher:</b>\s+<span .*?>(.*?)</span>',html)
                if puber:
                    publisher=puber[0]
                lan=re.findall('Language:</b>\s+<span .*?>(.*?)</span>',html)
                if lan:
                    language=lan[0]
                we=re.findall('Weight:</td><td width="80%" valign="top">(.*?)</td>',html,re.S)
                if we:
                    weight=we[0]
                det=re.findall('<.*?xml version="1.0" encoding="utf-8".*?>(.*?)<table',html,re.S)
                if det:
                    details=det[0].replace('<b>','').replace('</b>','').replace('<br/>',' ')
                results=re.findall('<h2 class="PDP_itemConditionTitle">(.*?)</h2>.*?<table cellpadding="0" cellspacing="0" class="PDP_itemList">(.*?)</table>',html,re.S)
                condition=[]
                for i in range(len(results)):
                    tu=[]
                    tu.append(results[i][0])
                    prices=re.findall('<td><span class="PDP_itemPrice">(.*?)</span></td>.*?<td><span class="PDP_itemPrice">(.*?)</span></td>',str(results[i]),re.S)
                    if prices:
                        tu.append(prices[0][0])
                        tu.append(prices[0][1])
                        condition.append(tu)
                    else:
                        prices=re.findall('<td><span class="PDP_itemPrice">(.*?)</span></td>',str(results[i]),re.S)
                        if prices:
                            tu.append(prices[0])
                            tu.append('')
                            condition.append(tu)
                info ={'ISBN':isbn,'ISBN-13':isbn13,'condition':condition,'weight':weight,'format':book_format,'language':language,'publisher':publisher,'author':author,'publish time':publish_time,'details':details,'title':title,'url':book_url}
                ff.write(str(info) + '\n')
                print (info)
            except BaseException as e:
                with open('./result/'+opt[0]+'/get_book_info_fail.txt','aw') as fff:
                    fff.write(book_url+'|'+filename + '\n')
                print (e)
                logger2.exception(str(e))
    print ('---------------------get_book_info end----------------------')
'''
    获取书籍信息
'''
if __name__ == '__main__':
    global opt
    opt=config.opt.split('|')
    logger1.info(opt[0]+'get book info begin')
    filenames = os.listdir('./result/'+opt[0]+'/book/')
    #filenames=filenames[:40]
    #get_book_info(filenames[0])
    pool = Pool(2)
    pool.map(get_book_info,filenames)
    pool.close()
    pool.join()

    os.system('nohup python classify_book_info.py &')
    logger1.info(opt[0]+'get book info success')
