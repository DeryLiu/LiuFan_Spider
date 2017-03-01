import sys
from Tools import get_html,ALL_CONFIG
import requests
from selenium import webdriver

sys.setrecursionlimit(1000000)
import time
import datetime
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



logging.config.fileConfig("./log/logging.conf")    # 采用配置文件  
logger1 = logging.getLogger("logger1")   
logger2 = logging.getLogger("logger2") 

url="http://search.half.ebay.com/[isbn]_W0QQmZbooksQQ_trksidZp2919Q2em1447Q2el2686"#"http://search.half.ebay.com/[isbn]_W0QQmZbooks"



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
def get_html(url):
    user_agent_list = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/ Safari/530.5",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-US) AppleWebKit/530.6 (KHTML, like Gecko) Chrome/ Safari/530.6",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-US) AppleWebKit/530.9 (KHTML, like Gecko) Chrome/ Safari/530.9",
        "Mozilla/5.0 (Macintosh; U; Mac OS X 10_5_7; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/ Safari/530.5",
        "Mozilla/5.0 (Macintosh; U; Mac OS X 10_6_1; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/ Safari/530.5",
        "Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
        "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13(KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; de) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.30 Safari/525.13",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.30 Safari/525.13",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.6 Safari/525.13",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.6 Safari/525.13",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.151.0 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.151.0 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.151.0 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.152.0 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.152.0 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.153.0 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.153.0 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.153.1 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.3.154.6 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.3.154.9 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.3.155.0 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/528.4 (KHTML, like Gecko) Chrome/0.3.155.0 Safari/528.4",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.4.154.18 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.4.154.31 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.39 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.42 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.43 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.43 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.43 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.43 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.46 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.48 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.50 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.50 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19"
        ]
    user_agent = random.choice(user_agent_list)
    # headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #            'Accept-Encoding':'gzip, deflate',
    #            'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    #            'Connection':'keep-alive',
    #            'Cookie':'dp1=btzo/-1e05865cad8^u1p/QEBfX0BAX19AQA**5a46f048^bl/CN5c2823c8^pbf/%238000000000005a46f048^; nonsession=CgADLAAJYZcPQNTkAygAgYcu+SGIyY2E0YmE3MTU3MGE3ZTMzMzU0YmI4NGZlNjJkYTYxECyjyQ**; npii=btguid/b2ca4ba71570a7e33354bb84fe62da615a46f053^cguid/b2ca59a31570a8835f814834f98f3e895a46f053^; s_vsn_prodhalf_1=416988692873; __utma=24000931.2022708610.1476173403.1481089478.1483061836.51; __utmz=24000931.1476173403.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); minhashguid=03261178-4c88-c4a6-cae9-6b8167e8e659; ebay=%5Edv%3D5865bcc5%5Esbf%3D%2310000000000%5Ecos%3D11%5Ecv%3D15555%5Ejs%3D1%5E; cssg=4d5fb2551590a7954bf394f3fae2df5f; s=CgAD4ACBYZw5INGQ1ZmIyNTUxNTkwYTc5NTRiZjM5NGYzZmFlMmRmNWaCM+MZ; __utmb=24000931.18.10.1483061836; __utmc=24000931; __utmt=1',
    #            'Host':'product.half.ebay.com',
    #            # 'Referer':'http://product.half.ebay.com/Creative-Haven-Coloring-Bks-Creative-Haven-Owls-Coloring-Book-by-Marjorie-Sarnat-2015-Paperback/208605589&tg=info',
    #            # 'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0'
    #            'User-Agent':user_agent
    #            }
    headers = {'User-Agent':user_agent}
    proxy_list = ['192.126.192.144:8800','89.32.70.9:8800','166.88.105.188:8800','89.32.64.244:8800','108.186.244.101:8800','173.44.219.22:8800',
                  '173.44.218.137:8800','192.126.131.176:8800','166.88.105.69:8800','45.33.157.189:8800','192.126.190.75:8800','166.88.106.157:8800',
                  '166.88.105.81:8800','173.44.218.134:8800','108.186.244.167:8800','89.32.66.16:8800','108.186.244.73:8800','192.126.148.168:8800',
                  '89.32.64.127:8800','89.32.66.128:8800','166.88.105.165:8800','192.126.181.80:8800','89.32.64.96:8800','45.33.157.8:8800',
                  '89.32.66.130:8800','192.126.192.238:8800','89.32.64.95:8800','192.126.148.108:8800','89.32.66.54:8800','173.44.218.108:8800',
                  '192.126.190.182:8800','89.32.64.248:8800','173.44.219.92:8800','192.126.181.85:8800','216.158.209.81:8800','166.88.105.239:8800','173.44.218.208:8800',
                  '173.44.218.72:8800','173.44.219.67:8800','192.126.131.179:8800','89.32.70.101:8800','166.88.106.30:8800','173.44.219.64:8800',
                  '173.44.218.22:8800','192.126.148.24:8800','166.88.105.212:8800','89.32.70.180:8800','192.126.131.77:8800','192.126.148.166:8800',
                  '166.88.106.246:8800','192.126.190.202:8800','166.88.106.124:8800','89.32.66.25:8800','173.44.219.179:8800','192.126.181.65:8800',
                  '89.32.64.151:8800','89.32.66.198:8800','108.186.244.229:8800','192.126.190.129:8800','192.126.131.149:8800']
    proxy = random.choice(proxy_list)
    proxies = {
        'http:': 'http://' + proxy,
        'https:': 'http://' + proxy
    }
    #----------------------------------------------------------------------
    # try:
    #     headers['User-Agent']=get_list_random(headers['User-Agent'])
    #     req = urllib2.Request(url,headers=headers)
    #     resp = urllib2.urlopen(req, timeout=20)
    #     html = resp.read()
    #     return html
    # except Exception as e:
    #     print 'error:', str(e)
    #     logger2.error(str(e))
    #     get_html(url)
    #----------------------------------------------------------------------
    try:
        r = requests.get(url, proxies=proxies,headers=headers,timeout=20)
        html = r.text
        return html

    except Exception as e:
        print ('error:', str(e))
        logger2.error(str(e))
        get_html(url)

'''
url：http://search.half.ebay.com/[isbn]_W0QQmZbooks
    获取书籍信息
'''
def get_book_info(isbn):

    url="http://search.half.ebay.com/"+isbn.replace("\n", "")+"_W0QQmZbooksQQ_trksidZp2919Q2em1447Q2el2686"
    print (url)
    time.sleep(2.5)
    html=get_html.get_html(url)

    if html and -1==html.find("No products found for"):
        if -1==html.find("Security Measure"):
            try:
                isbn13=''
                isbn=re.findall(r'ISBN-10:</b>\s+<span class=""><a href=.*? class="pdplinks">(.*?)</a>',html,re.S)
                if isbn:
                    isbn=isbn[0]
                else:
                    isbn=''
                isbn_13=re.findall(r'ISBN-13:</b>\s+<span class=""><a href=.*? class="pdplinks">(.*?)</a>',html,re.S)
                if isbn_13:
                    isbn13=isbn_13[0]
                weight=""
                we=re.findall(r'Weight:</td><td width="80%" valign="top">(.*?)</td>',html,re.S)
                try:
                    auther_list = re.findall(r'<span class="pdplinks">(.*?)</a>', html, re.S)
                    print (auther_list)
                    auther = str(auther_list).split('class="pdplinks">')[1]
                    print (auther)
                    auther = auther.split('<')[0]
                    auther.replace("']",'')
                except:
                    auther_list = re.findall(r'<span class="pdplinks">(.*?)</span>',html,re.S)
                    auther = re.findall(r'>(.*?)</a>',str(auther_list),re.S)
                    auther = str(auther).replace("']",'')
                    # auther = str(auther)

                if we:
                    weight=we[0]
                if weight=="":   #重量为空值，过滤掉
                    delete_file.write(isbn13+"\n")
                    delete_file.flush()
                else:                    
                    weight_float=float(weight.replace("oz","").strip())
                    if weight_float>60 or weight_float==0: #重量大于60或为0，过滤掉
                        delete_file.write(isbn13+"\n")
                        delete_file.flush()
                    else:
                        results=re.findall('<h2 class="PDP_itemConditionTitle">(.*?)</h2>.*?<table cellpadding="0" cellspacing="0" class="PDP_itemList">(.*?)</table>',html,re.S)
                        if results:
                            condition={"Brand New":"11",
                                       "Like New":"1",
                                       "Very Good":"2",
                                       "Good":"3",
                                       "Acceptable":"4"}
                            for i in range(len(results)):
                                book_info=[]
                                shelf_info=[]#上架信息
                                
                                book_info.append(isbn)
                                book_info.append(isbn13)
                                book_info.append(weight)
                                book_info.append(auther)
                                book_info.append(results[i][0])

                                #上架SKU
                                sku=isbn+"_"+condition[results[i][0]] + "_O_MM"
                                shelf_info.append(sku)
                                shelf_info.append(isbn)
                                shelf_info.append("1")
                                #对店铺做排除
                                prices=re.findall('<td><span class="PDP_itemPrice">(.*?)</span></td>.*?<td><a class="PDP_sellerName" href=".*?">(.*?)</a></td>',str(results[i]),re.S)
                                exclude_seller=['alibris_books_01','alibris_books_02','alibris_books_03','alibris_books_04','alibris_books_05',
                                                'alibris_books_06','alibris_books_07','alibris_books_08','alibris_books_09','alibris','alibris_movies','labsbooks11']
                                price_float=0.0#采购价格

                                if len(prices)==1:#condition下只有一个价格
                                    price_float=float(prices[0][0].replace("$","").replace(",",""))
                                    if prices[0][1] not in exclude_seller:
                                        book_info.append(prices[0][0])        
                                    else:
                                        break
                                elif len(prices)==2:#conditon下有两个价格
                                    count=0
                                    for j in range(2):
                                        if prices[j][1] not in exclude_seller:
                                            book_info.append(prices[j][0])
                                            orig_price=prices[j][0]#记录适合条件的最高价
                                            count+=1
                                    if count==0:
                                        break
                                    else:
                                        #采购价格
                                        price_float=float(orig_price.replace("$","").replace(",",""))
                                                                   
                                else:
                                    count=0
                                    for j in range(len(prices)):
                                        if prices[j][1] not in exclude_seller:
                                            book_info.append(prices[j][0]) 
                                            orig_price=prices[j][0]#记录适合条件的最高价
                                            count+=1
                                        if count==2:
                                            break
                                    if count==0:
                                        break
                                    else:
                                        #采购价格
                                        price_float=float(orig_price.replace("$","").replace(",",""))
                                        
                                #上架价格
                                if price_float>1:
                                    p1=(price_float+3.99)*1.5
                                    p2=price_float+23.99
                                
                                    price=str(p1>p2 and p1 or p2)
                                    shelf_info.append(price)
                                    shelf_info.append(price)
                                    # shelf_info.append(auther)
                                    shelf_info.append("8888800")
                                    shelf_info.append(condition[results[i][0]])
                                    shelf_info.append("1")
                                    shelf_info.append("1")
                                    shelf_info.append("N")
                                    shelf_info.append("5")
                                else:
                                    lock.acquire()
                                    delete_file.write("\t".join(book_info)+"\n")
                                    delete_file.flush()
                                    lock.release()
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
                                onshelf_file.write("\t".join(shelf_info)+"\n")
                                onshelf_file.flush()
                                lock.release()
                            print ("success:",isbn)
                            lock.acquire()
                            success_isbn_file.write(isbn13+"\n")
                            success_isbn_file.flush()
                            lock.release()
                        else:
                            print ("offshelf:",isbn)
                            lock.acquire()
                            offshelf_isbn_file.write(isbn13+"\n")
                            offshelf_isbn_file.flush()
                            lock.release()
            except BaseException as e:
                print (isbn,e)
                logger2.exception(str(e))
        else:
            lock.acquire()
            not_crawl_file.write(isbn)
            not_crawl_file.flush()
            lock.release()
    else:
        lock.acquire()
        not_list_file.write(isbn)
        not_list_file.flush()
        lock.release()

    #driver.quit()

def create_titles(filename,titles):
    f = open(filename,"w")
    f.write("\t".join(titles)+"\n")
    f.flush()
    f.close()

def snatch_book_info(asinfile,shelf_file,info_file):
    '''根据isbn更新half.com价格''' 
    global result_file#结果文件
    global onshelf_file#上架信息结果文件    
    global success_isbn_file
    global offshelf_isbn_file
    global not_crawl_file
    global not_list_file
    global delete_file#记录重量不合条件的ISBN，和采购价低于1的书籍信息
    global lock
    lock = Lock() 

    result_file=open(info_file,"w")
    onshelf_file=open(shelf_file,"w")
    success_isbn_file=open("./Data/snatch/info/success_isbn.txt","w")
    offshelf_isbn_file=open("./Data/snatch/info/offshelf_isbn.csv","w")
    not_crawl_file=open("./Data/snatch/info/not_crawl.txt","w")
    not_list_file = open("./Data/snatch/info/not_found.txt","w")
    delete_file=open("./Data/snatch/info/delete_isbn.txt","w")
    
    titles=['ISBN','ISBN13','weight','auther','condition','price','sec_price']
    shelf_titles=['sku','product-id','product-id-type','price','minimum-seller-allowed-price','maximum-seller-allowed-price','item-condition','quantity','will-ship-internationally','expedited-shipping','leadtime-to-ship']
    create_titles(info_file, titles)
    create_titles(shelf_file, shelf_titles)
    #取asin列表
#     path="./snatch/asin"
#     isbns=get_isbns(path)
    asin_file = open(asinfile)
    asins = asin_file.readlines()
#    asins = asins[:100]
#     print asins
    
    pool = Pool(20)
    pool.map(get_book_info,asins)
    pool.close()
    pool.join()
    
    result_file.close()
    onshelf_file.close()
    success_isbn_file.close()
    offshelf_isbn_file.close()
    not_list_file.close()
    not_crawl_file.close()
    delete_file.close()
    
def send_email(infofile):
    #创建一个带附件的实例
    msg = MIMEMultipart()
    #构造附件1
    att1 = MIMEText(open(infofile, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="new_info8.zip"'#这里的filename可以任意写，写什么名字，邮件中显示什么名字
    msg.attach(att1)
    #加邮件头
    #to_list=['liz0505@starmerx.com','lujuan@starmerx.com','lily@starmerx.com','jiping@starmerx.com']#发送给相关人员
    # to_list=['hengwei@starmerx.com','miaomiao@starmerx.com','zhaolei@starmerx.com']
    to_list=['hengwei@starmerx.com','1955725903@qq.com']
    msg['to'] = ';'.join(to_list)
    msg['from'] = 'hengwei@starmerx.com'
    msg['subject'] = 'half新抓Part8'
    #发送邮件
    try:
        server = smtplib.SMTP()
        server.connect('smtp.exmail.qq.com')
        server.login('hengwei@starmerx.com','Lianyu2016')#XXX为用户名，XXXXX为密码
        server.sendmail(msg['from'], to_list,msg.as_string())
        print ('发送成功',infofile)
    except Exception as e:
        print ('发送失败',e)
        logger2.error(str(e))
        #server.quit()
        send_email(infofile)
    finally:
        server.quit()

    
if __name__=="__main__":
    try:
        t1 = datetime.datetime.now()
        logger1.info('start:snatch_book_info()')
        info_file = "./Data/snatch/info/half_info8.csv"
        shelf_file="./Data/snatch/info/onshelf_info8.csv"
        send_file="new_info8.zip"
        asinfile="./Data/snatch/total_asin_offshelf_part8.txt"

        snatch_book_info(asinfile,shelf_file,info_file)

        os.system("zip new_info8.zip ./Data/snatch/info/*.*")
        # send_email(send_file)
        logger1.info('over:snatch_book_info()')
        t2 = datetime.datetime.now()
        print ('开始时间：',t1)
        print ('结束时间：',t2)
    except Exception as e:
        print (e)
        logger2.error(str(e))
    
