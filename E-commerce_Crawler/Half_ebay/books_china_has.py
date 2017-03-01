'''
Created on 2016年2月24日

@author: zhengjie
'''
import time
import datetime
import logging.config 
from multiprocessing import Lock, Pool
import re
import requests

from Tools.util import httptools


logging.config.fileConfig("./log/logging.conf")    # 采用配置文件  
logger1 = logging.getLogger("logger1")
logger2 = logging.getLogger("logger2") 


def handle(line):
    try:
        '''
        us_asin = eval(line)['asin']
        isbn = eval(line)['isbn']
        us_price = eval(line)['price']
        '''
        us_asin=line.replace("\n","")
        isbn=''
        logger1.info(us_asin)
        time.sleep(1)
        cn_info=[]
        cn_info.append(isbn)
        cn_info.append(us_asin)
        if isbn == '':
            url = 'https://www.amazon.cn/dp/' + us_asin
        else:
            url = 'https://www.amazon.cn/s/ref=nb_sb_noss?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=search-alias%3Dstripbooks&field-keywords=' + isbn

        print (url)
        html = tool.gethtmlproxy(url)
#         html = get_html_src(url)
#         html = get_html().gethtml(url)

        print ('handling...')
        #验证码页面
        if html == '' or -1!= html.find('<title dir="ltr">Amazon CAPTCHA</title>'):
            with open('1.html','w') as h:
                h.write(html)
            lock.acquire()
            captcha_url_file.write(us_asin+'\n')
            captcha_url_file.flush()
            lock.release()
            return
        #下架产品
        if html=='404 error':
            lock.acquire() 
            not_list_file.write(line)
            not_list_file.flush()
            lock.release()
            #print 'product not found'
            return
        if '没有找到任何与' in html:
            lock.acquire() 
            not_list_file.write(line)
            not_list_file.flush()
            lock.release()
            print ('product not found-----------')
            return
        #没有抓下来的页面
        if html=='time out or other errors':
            lock.acquire()
            not_crawl_file.write(line)
            not_crawl_file.flush()
            lock.release()
            return
        
        if isbn == '':
            cn_asin = us_asin
            cn_info.append(cn_asin)
            #cn_info.append(us_price)
            
            price = re.search('<span class="a-color-base">.*?<span class="a-color-price">.*?￥(.*?)\s+</span>',html,re.S)
            if price:
                price = price.group(1)
            else:
                price = re.search('<div class="a-text-center a-spacing-mini"><a href=".*?condition=new">全新品.*?￥(.*?)</span>',html)
                if price:
                    price = price.group(1)
                else:
                    price = re.search('<b class="priceLarge" >.*?￥ (.*?)\s+</b>',html,re.S)
                    if price:
                        price = price.group(1)
                    else:
                        price = re.search('来自 ￥(.*?)\s+</span>',html,re.S)
                        if price:
                            price = price.group(1)
                        else:
                            price = ''
            print (price)
            cn_info.append(price) 
                
            weight = re.search('<li><b>\s+商品重量: .*?</b>\s+(.*?)\s+</li>',html,re.S)
            if weight:
                weight = weight.group(1)
            else:
                weight = re.search('商品重量: (.*?) 品牌',html)
                if weight:
                    weight = weight.group(1)
                else:
                    weight = ''
            cn_info.append(weight)
               #########################20160725添加——抓取作者########################
            author_part=re.findall('<div id="byline".*?>(.*?)</div>',html,re.S)[0]
            author=re.findall('<a class="a-link-normal" href=".*?">(.*?)</a>.*?<a class="a-link-normal" href=".*?">(.*?)</a>',author_part,re.S)
            if author:
                author=author[0]
                for i in range(len(author)):
                    cn_info.append(author[i])
            else:
                author=re.findall('<a class="a-link-normal" href=".*?">(.*?)</a>',author_part,re.S)[0]
                cn_info.append(author)
               ##################################################################### 
        else:
            cn_asin = re.search('<input type="hidden" name="asin" value="(.*?)"',html)
            if cn_asin:
                cn_asin = cn_asin.group(1)
            else:
                cn_asin = re.search('<li id="result_0" data-asin="(.*?)"',html).group(1)
                    
            cn_info.append(cn_asin)
            #cn_info.append(us_price)
            
            new_url = 'https://www.amazon.cn/dp/' + str(cn_asin)
            html1 = tool.gethtmlproxy(new_url)
#             html1 = get_html_src(new_url)
#             html1 = get_html().gethtml(new_url)
            try:
                price = re.search('<span class="a-color-base">\s+<span class="a-color-price">.*?￥(.*?)\s+</span>',html1,re.S)
                if price:
                    price = price.group(1)
                else:
                    price = re.search('<div class="a-text-center a-spacing-mini"><a href=".*?condition=new">全新品.*?￥(.*?)</span>',html1)
                    if price:
                        price = price.group(1)
                    else:
                        price = re.search('<b class="priceLarge" >.*?￥ (.*?)\s+</b>',html1,re.S)
                        if price:
                            price = price.group(1)
                        else:
                            price = re.search('来自 ￥(.*?)\s+</span>',html1,re.S)
                            if price:
                                price = price.group(1)
                            else:
                                price = ''
                                       
                weight = re.search('<li><b>\s+商品重量: .*?</b>\s+(.*?)\s+</li>',html1,re.S)
                if weight:
                    weight = weight.group(1)
                else:
                    weight = re.search('商品重量: (.*?) 品牌',html1)
                    if weight:
                        weight.group(1)
                    else:
                        weight = ''
            except:
                price = 'not_found'
                weight = 'not_found'
                with open('./info_cn/get_price_fail.txt','aw') as f:
                    f.write(cn_asin + '\n')
            cn_info.append(price)
            cn_info.append(weight)  
               #########################20160725添加——抓取作者########################
            author_part=re.findall('<div id="byline".*?>(.*?)</div>',html,re.S)[0]
            author=re.findall('<a class="a-link-normal" href=".*?">(.*?)</a>.*?<a class="a-link-normal" href=".*?">(.*?)</a>',author_part,re.S)
            if author:
                author=author[0]
                for i in range(len(author)):
                    cn_info.append(author[i])
            else:
                author=re.findall('<a class="a-link-normal" href=".*?">(.*?)</a>',author_part,re.S)[0]
                cn_info.append(author)
               ##################################################################### 
        print (cn_info)
            
        lock.acquire()
        result_file.write("\t".join(cn_info)+"\n")
        result_file.flush()
        success_asin_file.write(line)
        success_asin_file.flush()
        lock.release()
    except Exception as e:
        print (us_asin,e)
        logger2.error(str(us_asin)+' '+str(e))
        

def create_titles(filename,titles):
    f = open(filename,"w")
    f.write("\t".join(titles)+"\n")
    f.flush()
    f.close()

def get_cn_buybox(asinfile,buyboxinfofile):
    print ("run start...")
    global result_file#结果文件
    global captcha_url_file#yan zheng ma ye mian
    global not_list_file#yi xia jia ye mian
    global not_crawl_file#抓取3次后失败，没有抓取到结果的页面
    global success_asin_file
    global lock,tool
    
    lock = Lock()   
    tool = httptools.httptools('cn')
    captcha_url_file = open("./info_cn/captcha_url.txt","w")
    not_list_file = open("./info_cn/not_found.txt","w")
    not_crawl_file = open("./info_cn/not_crawl.txt","w")
    success_asin_file = open("./info_cn/success_asin.txt","w")
    
    #titles = ['ISBN','us_asin','cn_asin','us_price','cn_price','weight','author','translator']
    
    titles = ['ISBN','us_asin','cn_asin','cn_price','weight','author','translator']
    create_titles(buyboxinfofile, titles)
    result_file = open(buyboxinfofile,"aw")
    
    asin_file = open(asinfile)
    lines = asin_file.readlines()
     
    pool = Pool(20)
    pool.map(handle,lines)
    pool.close()
    pool.join()
    
    result_file.close()
    captcha_url_file.close()
    not_list_file.close()
    not_crawl_file.close()
    success_asin_file.close()
    
    print ("run over")

if __name__ == '__main__':
    try:
        t1 = datetime.datetime.now()
        logger1.info('start:get_cn_buybox()')
        # asinfile = './result/asins/asin_info.txt'
        buyboxinfofile = './info_cn/cn_books_info.csv'

        asinfile = './Data/snatch/asin/asins.csv'

        get_cn_buybox(asinfile,buyboxinfofile)
        logger1.info('over:get_cn_buybox()')
        t2 = datetime.datetime.now()
        print ('开始时间：',t1)
        print ('结束时间：',t2)
    except Exception as e:
        print (e)
        logger2.error(str(e))
