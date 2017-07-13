import logging.config
from multiprocessing import Pool, Lock
import re, os
import requests
import datetime
import time
import random
import subprocess

# from get_asins import get_asins
from Tools.util import httptools


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

# def get_html_src(url):
#     try:
#         time.sleep(2)
#         headers = {"User-agent":["Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
#                                  "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)",
#                                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/601.5.17 (KHTML, like Gecko) Version/9.1 Safari/601.5.17",
#                                  "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729)",
#                                  "Mozilla/5.0 (Windows; U; Windows NT 5.2; zh-CN) AppleWebKit/534.31 (KHTML, like Gecko) Chrome/17.0.558.0 Safari/534.31 baidubrowser/7.5.22.0 (Baidu; P1 4.3)",
#                                  "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
#                                  "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0); 360Spider",
#                                  "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
#                                  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
#                                  "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"]}
#         headers['User-Agent']=get_list_random(headers['User-Agent'])
#         req = urllib2.Request(url, None, headers)
#         page = urllib2.urlopen(req, timeout=10)
#         html_src = page.read()
#         return html_src
#     except Exception,e:
#         print str(e)
#         if "404" in str(e):
#             return '404 error'
#         else:
#             return 'time out or other errors'
 
def get_count(url):#没有解析出count的url记录下来。
    html = tool.gethtmlproxy(url)
        
    try:

#         html = get_html_src(url) 
        if html == '' or -1!= html.find('Sorry, we just need to make sure you'):
            lock.acquire()
            captcha_url_file.write(url + '\n')
            captcha_url_file.flush()
            lock.release()
            return
        if html == '404 error':
            lock.acquire() 
            not_list_file.write(url + '\n')
            not_list_file.flush()
            lock.release()
            #print 'product not found'
            return
        #没有抓下来的页面
        if html == 'time out or other errors':
            lock.acquire()
            not_crawl_file.write(url + '\n')
            not_crawl_file.flush()
            lock.release()
            return 
        num = re.search('<h2 id="s-result-count".*?>1-60 of (.*?) results',html)
        if num == None:
            num = re.search('<h2 id="s-result-count".*?>(.*?) result',html)
                
             
        if num != None:
            if -1 !=html.find("500+"):
                #页面不显示产品实际数量，只有500+
                return 500
            elif num.group(1)=="Showing":
                #页面没有产品数量，显示Showing results for ……
                return 500
            else:
                num = int(num.group(1).replace(',',''))
                return num
        else:
            if -1 !=html.find("500+"):
                return 500
            elif 'did not match any products.' in html:
                lock.acquire()
                f_no_product.write(url + '\n')
                f_no_product.flush()
                lock.release()
                return
            else:
                with open('get_count_fail.txt','aw') as f:
                    f.write(url + '\n')
                return
    except Exception as e:
        logger2.error(url + ':' + str(e))
#         with open("showing.html","w") as f:
#             f.write(html)
         
'''
url :https://www.amazon.com/gp/search/ref=sr_nr_n_0?fst=as%3Aoff&rh=n%3A283155%2Cn%3A!1000%2Cn%3A10159375011%2Cp_36%3A100-&bbn=266162&ie=UTF8&qid=1472547590&rnid=266162&lo=stripbooks
'''
def dichotomy(low,high,id):        
    try:
        base_url = 'https://www.amazon.com/gp/search/ref=sr_nr_n_0?fst=as%3Aoff&rh=n%3A283155%2Cn%3A!1000%2Cn%3A[id]%2Cp_36%3A[low]-[high]&bbn=266162&ie=UTF8&qid=1472547590&rnid=266162&lo=stripbooks'
        url = base_url.replace('[id]', id).replace('[low]',str(low)).replace('[high]', str(high))
#         print url
        count = get_count(url)
        if count == None:
            return
        if count < 500:
            lock.acquire()
            f_price_url.write(url + '\t' + str(count) + '\n')
            f_price_url.flush()
            lock.release()
            print (url,':',count)
        else:
            if high!='':
                mid=int((int(low)+int(high))/2)
            else:
                mid=low+10000
             
            url_low = base_url.replace('[id]', id).replace('[low]',str(low)).replace('[high]', str(mid))
            count_low = get_count(url_low)
            if count_low == None:
                return
            if count_low < 500:
                lock.acquire()
                f_price_url.write(url_low + '\t' + str(count_low) + '\n')
                f_price_url.flush()
                lock.release()
                print (url_low,':',count_low)
            else:
                if mid - low == 1:   
                    lock.acquire()
                    f_price_url.write(url_low + '\t' + str(count_low) + '\n')
                    f_price_url.flush()
                    lock.release()
                    print (url_low,':',count_low)
                else:
                    dichotomy(low,mid,id)
                     
            url_high = base_url.replace('[id]', id).replace('[low]',str(mid)).replace('[high]', str(high))
            count_high = get_count(url_high)
            if count_high == None:
                return
            if count_high < 500:
                lock.acquire()
                f_price_url.write(url_high + '\t' + str(count_high) + '\n')
                f_price_url.flush()
                lock.release()
                print (url_high,':',count_high)
            else:
                if high - mid == 1:   
                    lock.acquire()
                    f_price_url.write(url_high + '\t' + str(count_high) + '\n')
                    f_price_url.flush()
                    lock.release()
                    print (url_high,':',count_high)
                else:
                    dichotomy(mid,high,id)
    except Exception as e:
        logger2.error(url + '\t' + str(e))
 
def handle_url(cate_id):
    global f_price_url,f_no_product,captcha_url_file,not_list_file,not_crawl_file
    
    try:
        low=0
        high=''
        st=time.time()
        #确保以id命名的文件夹存在
        dir_name="./result/"+cate_id
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        #拆分价格段
        logger1.info('start dichotomy...'+cate_id)
        f_price_url = open(dir_name+"/price_url.txt",'w')
        f_no_product =  open(dir_name+"/no_product.txt",'w')
        captcha_url_file = open(dir_name+"/captcha_url",'w')
        not_list_file = open(dir_name+"/not_found.txt",'w')
        not_crawl_file = open(dir_name+"/not_crawl.txt",'w')
        
        dichotomy(low,high,cate_id)
        
        f_price_url.close()
        f_no_product.close()
        captcha_url_file.close()
        not_list_file.close()
        not_crawl_file.close()
        logger1.info('end dichotomy...'+cate_id)
        #获取asin
        logger1.info('start get_asins...'+cate_id)
#         get_asins(dir_name)
        subprocess.call("nohup python get_asins.py "+dir_name+" &",shell=True)
        logger1.info('end get_asins...'+cate_id)

        et=time.time()
        print ("Category ID:",cate_id," Cost:",et-st)
        
    except Exception as e:
        logger2.error(cate_id + '\t' + str(e))

def get_price_url():  
    global lock,tool
    tool = httptools.httptools('com')
    lock = Lock()
    
    categories_file=open('./result/categorys.txt')
    lines=categories_file.readlines()
    cate_ids=[]
    for line in lines:
        split=line.replace("\n","").split("|")
        if -1!=split[1].find("True"):
            cate_ids.append(split[0])
             
#     print len(cate_ids)
#     cate_ids=cate_ids[:1]
     
    pool=Pool(5)
    pool.map(handle_url,cate_ids)  
    pool.close()
    pool.join()  
     

if __name__=='__main__':
    try:
        t1 = datetime.datetime.now()
#         logger1.info('start get_price_url...')
        get_price_url()
#         logger1.info('over get_price_url')
        t2 = datetime.datetime.now()
        print ('开始时间：',t1)
        print ('结束时间：',t2)
    except Exception as e:
        print (e)
        logger2.error(str(e))

        
