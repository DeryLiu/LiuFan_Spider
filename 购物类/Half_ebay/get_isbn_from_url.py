import requests
import re
from io import StringIO
import gzip
import os
from multiprocessing import Pool,Lock
import logging
import logging.config
import time
import datetime
import random
from Tools import get_html,ALL_CONFIG
logging.config.fileConfig("./log/logging.conf")    # 采用配置文件  
logger1 = logging.getLogger("logger1")   
logger2 = logging.getLogger("logger2") 

def get_list_random(list_value):
    """
    :param list_value:原数组
    :return:数组的一个随机值
    """
    temp_index = random.randint(0, len(list_value) - 1)
    return list_value[temp_index]


'''
    获取网页的源代码
'''
# def get_html(url):
#     headers = {
#                 'User-Agent':[
#         'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
#         'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
#         "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
#         "Mozilla/4.0(compatible; MSIE 7.0b; Windows NT 6.0)",
#         "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)",
#         "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
#         "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; Media Center PC 3.0; .NET CLR 1.0.3705; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.1)",
#         "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; FDM; .NET CLR 1.1.4322)",
#         "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1; .NET CLR 2.0.50727)",
#         "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1)",
#         "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; Alexa Toolbar; .NET CLR 2.0.50727)",
#         "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; Alexa Toolbar)",
#         "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
#         "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.40607)",
#         "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322)",
#         "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.0.3705; Media Center PC 3.1; Alexa Toolbar; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"
#         "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8",
#         "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; Media Center PC 6.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C)",
#         "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.3; .NET4.0C; .NET4.0E; .NET CLR 3.5.30729; .NET CLR 3.0.30729; MS-RTC LM 8)",
#         "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)",
#         "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 3.0)",
#         "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; msn OptimizedIE8;ZHCN)",
#     ]}
#     try:
#         headers['User-Agent']=get_list_random(headers['User-Agent'])
#         req = urllib2.Request(url,headers=headers)
#         resp = urllib2.urlopen(req, timeout=10)
#         html = resp.read()
#         return html
#     except Exception as e:
#         print 'error:', str(e)
#         logger2.error(str(e))
#         get_html(url)

def get_book_isbn(url):
    try:
        time.sleep(2.5)
        html=get_html.get_html(url.replace("\n",""))
        if html and -1==html.find("Security Measure"):
            try:
                isbn13=''
                isbn=re.findall('ISBN-10:</b>\s+<span class=""><a href=.*? class="pdplinks">(.*?)</a>',html)
                if isbn:
                    isbn=isbn[0]
                else:
                    isbn=''
                isbn_13=re.findall('ISBN-13:</b>\s+<span class=""><a href=.*? class="pdplinks">(.*?)</a>',html)
                if isbn_13:
                    isbn13=isbn_13[0]
                results=re.findall('<h2 class="PDP_itemConditionTitle">(.*?)</h2>.*?<table cellpadding="0" cellspacing="0" class="PDP_itemList">(.*?)</table>',html,re.S)
                if results:
                    for i in range(len(results)):
                        book_info=[]
                        book_info.append(isbn)
                        book_info.append(isbn13)
                        book_info.append(results[i][0])
                        #对店铺做排除
                        prices=re.findall('<td><span class="PDP_itemPrice">(.*?)</span></td>.*?<td><a class="PDP_sellerName" href=".*?">(.*?)</a></td>',str(results[i]),re.S)
                        exclude_seller=['alibris_books_01','alibris_books_02','alibris_books_03','alibris_books_04','alibris_books_05',
                                        'alibris_books_06','alibris_books_07','alibris_books_08','alibris_books_09','alibris','alibris_movies']
                        if len(prices)==1:
                            if prices[0][1] not in exclude_seller:
                                book_info.append(prices[0][0])
                        elif len(prices)==2:
                            for i in range(2):
                              if prices[i][1] not in exclude_seller:
                                book_info.append(prices[i][0])                          
                        else:
                            count=0
                            for i in range(len(prices)):
                                if prices[i][1] not in exclude_seller:
                                    book_info.append(prices[i][0]) 
                                    count+=1
                                if count==2:
                                    break
#                         #对店铺不做排除                                                    
#                         prices=re.findall('<td><span class="PDP_itemPrice">(.*?)</span></td>.*?<td><span class="PDP_itemPrice">(.*?)</span></td>',str(results[i]),re.S)
#                         if prices:
#                             book_info.append(prices[0][0])
#                             book_info.append(prices[0][1])
#                         else:
#                             prices=re.findall('<td><span class="PDP_itemPrice">(.*?)</span></td>',str(results[i]),re.S)
#                             if prices:
#                                 book_info.append(prices[0])
#                                 book_info.append('')
                                
                        lock.acquire()
                        result_file.write("\t".join(book_info)+"\n")
                        result_file.flush()
                        lock.release()
                    print ("success:",isbn)
                    lock.acquire()
                    success_url_file.write(url)
                    success_url_file.flush()
                    lock.release()
                else:
                    print ("offshelf:",isbn)
                    lock.acquire()
                    offshelf_isbn_file.write(isbn+"\n")
                    offshelf_isbn_file.flush()
                    lock.release()
            except BaseException as e:
                print (isbn,e)
                logger2.exception(str(e))
        else:
            lock.acquire()
            not_crawl_file.write(url)
            not_crawl_file.flush()
            lock.release() 
    except Exception as e:
        print ('error:', str(e))
        logger2.error(str(e))

def create_titles(filename,titles):
    f = open(filename,"w")
    f.write("\t".join(titles)+"\n")
    f.flush()
    f.close()

def get_isbn_from_url(urlfile):
    global result_file#结果文件    
    global success_url_file
    global offshelf_isbn_file
    global not_crawl_file   
    global lock 
    
    info_file="./result/half_info.csv"
    result_file=open(info_file,"w")
    success_url_file=open("./result/success_url.txt","w")
    offshelf_isbn_file=open("./result/offshelf_isbn.txt","w")
    not_crawl_file=open("./result/not_crawl.txt","w")

    lock=Lock()
    
    logger1.info('start:get_isbn_from_url()')
    titles=['ISBN','ISBN13','condition','price','sec_price']
    create_titles(info_file, titles)    
    url_file=open(urlfile)
    urls=url_file.readlines()
#     urls=["http://product.half.ebay.com/The-20-20-Diet-Turn-Your-Weight-Loss-Vision-into-Reality-by-Phil-McGraw-2015-Hardcover/204200904&tg=info"]
       
    pool=Pool(20)
    pool.map(get_book_isbn,urls)
    pool.close()
    pool.join()
    
    result_file.close()
    not_crawl_file.close()
    logger1.info('end:get_isbn_from_url()')

if __name__ == "__main__":
    try:
        t1 = datetime.datetime.now()
 
        urlfile="./result/url.txt"  
            
        logger1.info('start:get_isbn_from_url()')
        get_isbn_from_url(urlfile)                
        logger1.info('end:get_isbn_from_url()')
        
        t2 = datetime.datetime.now()
        print ('开始时间：',t1)
        print ('结束时间：',t2)
    except Exception as e:
        print (e)
        logger2.error(str(e))