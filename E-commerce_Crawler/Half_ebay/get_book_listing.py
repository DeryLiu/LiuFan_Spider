import requests
import re
from io import StringIO
import gzip
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
#         #get_html(url)


'''
    获取品类下书籍列表
'''
def get_book_url(page):
        if os.path.exists('./result/'+opt[0])==0:
            os.mkdir('./result/'+opt[0])
        with open('./result/'+opt[0]+'/book_urls.txt','aw') as ff:
            url=opt[1]+'QQpgZ'+str(page)
            print (url)
            while True:
                html=get_html(url)
                if html:
                    real_page=re.findall('<b>Page (.*?)</b> of',html)
                    if real_page:
                        if str(page)==real_page[0]:
                            book_urls=re.findall('<div style="float:left;" itemscope="itemscope" itemtype="http://schema.org/SearchResultsPage"><b><a href="(.*?)">',html,re.S)
                            for book_url in book_urls:
                                ff.write(book_url+'\n') 
                            break 
                    elif -1!=html.find("Try again..."):
                        break


'''
    获取书籍品类url
'''
if __name__ == '__main__':
    global opt
    opt=config.opt.split('|')
    logger1.info(opt[0]+'get book listing begin')
    page=[i+1 for i in range(config.page)]

    pool = Pool(4)
    pool.map(get_book_url,page)
    pool.close()
    pool.join()

    sentence='sort ./result/'+opt[0]+'/book_urls.txt | uniq >./result/'+opt[0]+'/book_url.txt'
    status = os.system(sentence)
    #os.system('nohup python get_book_html.py &')
    logger1.info(opt[0]+'get book listing success')
