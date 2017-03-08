import codecs
import re
from Tools import get_html,ALL_CONFIG
import time
import pytz
from selenium import webdriver
from datetime import datetime,timedelta
from Tools.AMAZON_API.amazon_api.Amazon_api import Amazon_AWS,Amazon_MWS
import sys
from multiprocessing import Pool,Lock


#传入商品页面的html和商品的id
def get_info(html,itemsurl,sign):
    # itemsurl = str(items).split('>')[1]
    print (itemsurl)
    # driver.get(itemsurl)
    # html = driver.page_source  # 这就是返回的页面内容了

    items_info = []
    # print '-------------sign--------------'
    # sign = str(items).split('>')[0]
    items_info.append(sign)

    # print '------------itemsId------------'
    itemsId_list = re.findall(r'/dp/(.*?)/ref', itemsurl, re.S)
    if itemsId_list:
        itemsId = ''.join(itemsId_list)
    else:
        itemsId_list = re.findall(r'pd_rd_i=(.*?)&amp', itemsurl,re.S)
        itemsId = ''.join(itemsId_list)

    items_info.append(str(itemsId))

    print (itemsId)
    # 调用api
    # html = get_html.get_amazon_html_proxy(itemsurl)
    #----

#把itemsId页面的html传入get_info函数中，把失败的id重新存一个文件
def handle(items):
    # sign = str(items).split('>')[0]
    url = 'https://www.amazom.com/dp/'+items
    print (url)
    try:
        #商品详情页
        #获取每一个商品页面的html
        html = get_html.get_html(url)

        if html:
            #调用get_info函数，传入html
            print (html)
        else:
            print ('error')

    except Exception as e:
        with open('./Result/asin_is_exist/error.txt','a') as fail_url:
            fail_url.write(items+e+'\n')

#去重后的items的id文件
def start(items_file):

    global result_file, lock, titles,fr,ferr,item_file

    item_file = open(items_file, 'r')

    #调用函数create_titles
    result_file = open('./Result/asin_is_exist/really_not_exist.csv', 'aw')
    items_list = item_file.readlines()

    #把获取的url依次传入handle
    items = []
    for item in items_list:
        item = item.split('\n')[0]
        items.append(item)
        # get_info(item)

    lock = Lock()
    pool = Pool(1)
    #调用函数把items的url依次传入handle函数中爬虫
    pool.map(handle, items)
    pool.close()
    pool.join()

    item_file.close()
    result_file.close()

if __name__ == "__main__":

    start(ALL_CONFIG.ISASINEXIT_TESTAGAIN_FILE)
