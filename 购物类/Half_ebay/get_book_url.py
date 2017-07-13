import requests
import re
from io import StringIO
import gzip
import os
from multiprocessing import Pool,Lock
import logging
import logging.config
import datetime
import random
from Tools import get_html,ALL_CONFIG
import select
import config
import reload
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

def get_bookurl_by_cateurl(url):
    try:
        html=get_html.get_html(url)
        if html and -1==html.find("Security Measure"):
            pages=re.findall('<b>Page 1</b> of (.*?)<br>',html)
            if pages:
                pages=int(pages[0].replace(",",""))
                book_urls=re.findall('<div style="float:left;" itemscope="itemscope" itemtype="http://schema.org/SearchResultsPage"><b><a href="(.*?)">',html,re.S)
                for book_url in book_urls:
                    lock.acquire()
                    result_file.write(book_url+'\n')
                    result_file.flush()
                    lock.release()
            url=url+'QQpgZ'
            for page in range(2,pages):
                bookurl=url+str(page)
                print (bookurl)
                while True:
                    html=get_html(bookurl)
                    if html:
                        real_page=re.findall('<b>Page (.*?)</b> of',html)
                        if real_page:
                            if str(page)==real_page[0]:
                                book_urls=re.findall('<div style="float:left;" itemscope="itemscope" itemtype="http://schema.org/SearchResultsPage"><b><a href="(.*?)">',html,re.S)
                                for book_url in book_urls:
                                    lock.acquire()
                                    result_file.write(book_url+'\n')
                                    result_file.flush()
                                    lock.release()
                                break 
                        elif -1!=html.find("Try again..."):
                            break
        else:
            lock.acquire()
            not_crawl_file.write(url+"\n")
            not_crawl_file.flush()
            lock.release()  
    except Exception as e:
        print (e)
        logger2.error(str(e))
        
'''
    获取子品类下书籍列表
'''
def get_book_url(leafcates):
    global result_file#结果文件
    global not_crawl_file   
    global lock 
    
    result_file=open("./result/book_url.txt","w")
    not_crawl_file=open("./result/not_crawl.txt","w")

    lock=Lock()
    print (leafcates)
    pool=Pool(20)
    pool.map(get_bookurl_by_cateurl,leafcates)
    pool.close()
    pool.join()
    
    result_file.close()
    not_crawl_file.close()
'''
    获取子品类的URL
'''
def get_leaf_cate_url(option):
    try:
        url=option[1]
        print (url)
        html=get_html(url)
        f=open("except.html","w")
        f.write(html)
        if html:
            leafcates=re.findall('<td width="100%"><a href="(.*?)">.*?</a> ', html)
            if leafcates:
                return leafcates

        else:
            logger2.error("No leaf categories found")
            return []
    except Exception as e:
        print (e)
        logger2.error(str(e))
        
        
def modify_config(line):
    f=open('config.py')
    lines=f.readlines()
    f.close()
    lines[5]="category_line="+line+"\n"
    f=open('config.py','w')
    f.writelines(lines)
    f.flush()
    f.close()
    reload(config)
    command="sed -n '2,6p' config.py"
    lines=os.popen(command).read()
    print (lines)
        
'''
    获取书籍品类url
'''
if __name__ == '__main__':    
    try:
        global opt
        opt=config.opt.split('|')  
        t1 = datetime.datetime.now()
          
#         categoryfile="./result/cate_url.txt"
#         cate_list=select.select_category() 
            
        logger1.info('start:get_leaf_cate_url()')
        leafcates=get_leaf_cate_url(opt)                
        logger1.info('end:get_leaf_cate_url()')        
        logger1.info('start:get_book_url()')
        get_book_url(leafcates)        
        logger1.info('end:get_book_url()')
          
        t2 = datetime.datetime.now()
        print ('开始时间：',t1)
        print ('结束时间：',t2)
          
        sentence='sort ./result/book_url.txt | uniq >./result/url.txt'
        status = os.system(sentence)
        os.system('nohup python get_isbn_from_url.py &')
  
    except Exception as e:
        print (e)
        logger2.error(str(e))
        
#     try:
# #         global category
#         category_line=config.category_line 
#         t1 = datetime.datetime.now()
#          
#         categoryfile=open("./result/cate_url.txt")
#         categories= categoryfile.readlines()
#         category=categories[category_line]
#         print category
#         opt=category.split("|")
#            
#         logger1.info('start:get_leaf_cate_url()')
#         leafcates=get_leaf_cate_url(opt)                
#         logger1.info('end:get_leaf_cate_url()')        
#         logger1.info('start:get_book_url()')
#         get_book_url(leafcates)        
#         logger1.info('end:get_book_url()')
#           
#         t2 = datetime.datetime.now() 
#         print '开始时间：',t1
#         print '结束时间：',t2
#         
#         category_line+=1
#         modify_config(category_line)
#           
#         sentence='sort ./result/book_url.txt | uniq >./result/url.txt'
#         status = os.system(sentence)
#         os.system('nohup python get_isbn_from_url.py &')
#  
#     except Exception,e:
#         print e
#         logger2.error(str(e))
    