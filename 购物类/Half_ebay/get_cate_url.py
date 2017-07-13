import requests
import re
from io import StringIO
import gzip
import os
import logging
import logging.config
from Tools import get_html
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
  获取书籍品类url
'''
if __name__ == '__main__':
    if os.path.exists('./result')==0:
        os.mkdir('./result')
    logger1.info('get category url begin')
    with open('./result/cate_url.txt','aw') as f:
        try:
            f.truncate(0)
            base_category_url = 'http://books.half.ebay.com/'
            html=get_html.get_html(base_category_url)
            separator=re.findall('<div class="separator">.*?<ul class="metascateitems">(.*?)</ul>',html,re.S)[0].replace('\n','').replace('\t','').replace('\r','')
            cate_urls=re.findall('<li><a href="(.*?)">(.*?)</a></li>',separator)
            for cate_url in cate_urls:
                url=cate_url[0]
                cate=cate_url[1].replace('&amp;','&')
                f.write(url + '|'+cate + '\n')
            print ('-----------get category url successfuly--------------')
        except Exception as e:
            print ('error:', str(e))
            logger2.error(str(e))
    logger1.info('get category url success')
