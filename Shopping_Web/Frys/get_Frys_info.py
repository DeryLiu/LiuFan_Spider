import codecs
import re
from Tools import get_html
import time
import pytz
import random
from datetime import datetime,timedelta
from multiprocessing import Pool,Lock

# #把list洗乱
# def shuffle_list(list_name):
#
#     from random import shuffle
#     shuffle(list_name)
#     # 返回随机排序后的序列
#     return list_name
#
# #传入商品页面的html和商品的id
# def get_info(html):
#
#     items_info = []
#     print ('------------itemsId------------')
#     itemsId_list = re.findall(r'<div id="ProductAttributes">.*?<li style=.*?>(.*?)</li>.*?</div>',html,re.S)
#
#     itemsId = str(itemsId_list[0]).split('#')[1]
#     print (itemsId)
#     # items_info.append(str(itemsId))
#
#     # print ' ------------title------------'
#     title = itemsId_list[1]
#     print (title)
#     # items_info.append(str(title))
#
#     # print ' ------------Price------------'
#     price = re.findall(r'<label id="l_price1_value.*?>(.*?)</label>', html,re.S)
#     print (price[0])
#     # items_info.append(str(price[0]))
#
#     # print '------------Stock------------'
#     stock = re.findall(r'<div style="width:90%; float: left;">(.*?)</div>',html,re.S)
#
#     items_info.append(str(stock))
#
#     # print ' ------------brand------------'
#
#     brand = result_response['brand']
#     items_info.append(str(brand))
#
#
#
#     # ------------Reviews------------
#     # review = ''
#     # review_count = re.findall(r'<span id="acrCustomerReviewText" class="a-size-base">(.*?)</span>',html,re.S)
#     # print review_count+'======'
#     # review = str(review_count).split(' ')[0]
#     # items_info['reviews'] = review
#
#     # print ' ------------image------------'
#     image_list = result_response['image_list']
#     if image_list == []:
#         image_list = ['','','','','']
#     while len(image_list) < 5:
#         image_list.append("")
#
#     # print type(image_list)
#     images = image_list[:5]  # 最多取5张图片
#     items_info += images
#
#     #------------details------------
#     # 前有\xe2\x9c\x94     \xc2\xa0
#     details_Feature = result_response['detail']
#     details_list = details_Feature['Feature']
#
#     if isinstance(details_list, str):
#         details_list = [details_list]
#         print details_list
#
#     while len(details_list)<4:
#         details_list.append("")
#
#     details_list = details_list[:4]
#     for i in range(0,4):
#         details_list[i] = str(details_list[i]).replace('\n','').replace('\xe2\x9c\x94','').replace('\xc2\xa0','').replace('<br>','.').replace('</br>','')
#
#         if str(details_list[i]).find("Refurbished") == -1 or str(details_list[i]).find("used") == -1:
#             is_Refurbished = False
#         else:
#             is_Refurbished = True
#
#     items_info += details_list
#
#     # ------------Specification------------
#     Specification = result_response['description']
#     if Specification == None or len(Specification)>5000:
#         Specification = '\n'
#     if len(Specification)  <5000:
#         Specification = Specification[:1000]
#     Specification = ''.join(Specification)
#     Specification = Specification.replace('\n','').replace('\xe2\x9c\x94','').replace('\xc2\xa0','').replace('<b>','').replace('</b>','').replace('<br>','').replace('</br>','').replace('<br/>','')
#
#     items_info.append(str(Specification))
#     if str(Specification).find("Refurbished") == -1 or str(Specification).find("used") == -1:
#         is_Refurbished = False
#     else:
#         is_Refurbished = True
#
#     print '=====================END==================================='
#     print items_info
#
#
#     result_file.write("\t".join(items_info) + "\n")
#
#     print '============='
#     # f.flush()
#     item_file.flush()
#     result_file.flush()
#
#
# #把itemsId页面的html传入get_info函数中，把失败的id重新存一个文件
# def handle(itemsurl):
#     try:
#         #商品详情页
#         #获取每一个商品页面的html
#         html = get_html.get_PhantomJS_html(itemsurl)
#         # print html
#         # 获取每一个商品的asin
#         print html
#
#         if html:
#             #调用get_info函数，传入html
#             get_info(html)
#         else:
#             with open('./Result/get_html_fail.txt', 'aw') as h:
#                 h.write(itemsurl + '\n')
#
#     except Exception, e:
#         # print itemsurl, ":",  e
#         with open('./Result/fail_url.txt','aw') as fail_url:
#             fail_url.write(itemsurl+'\n')
#         # with open('./Result/no_except.txt', 'aw') as f:
#         #     f.write(itemsurl + '\n')
#
# #把items_last.txt文件中的字段制成表格
# def create_titles(filename, titles):
#     f = open(filename, "w")
#     f.write("\t".join(titles) + "\n")
#     #清除内部缓冲区
#     f.flush()
#     #关闭文件
#     f.close()
#
# #去重后的items的id文件
# def start(items_file,file_name):
#
#     global result_file, lock, titles,fr,ferr,item_file
#     titles = ['itemsId', 'price', 'stock', 'brand', 'title', 'img1', 'img2', 'img3', 'img4',
#               'img5', 'detail1', 'detail2', 'detail3', 'detail4', 'Specification']
#     item_file = open(items_file, 'r')
#
#     #调用函数create_titles
#     create_titles(file_name, titles)
#     result_file = open(file_name, 'aw')
#     items_list = item_file.readlines()
#     #把获取的url依次传入handle
#     items = []
#     for item in items_list:
#         item = item.split('\n')[0]
#         items.append(item)
#     lock = Lock()
#     pool = Pool(10)
#     #调用函数把items的url依次传入handle函数中爬虫
#     pool.map(handle, items)
#     pool.close()
#     pool.join()
#
#     item_file.close()
#     result_file.close()

def get_asin(base_url,page):
    #Electronics : Computers & Accessories : Monitors : Prime Eligible : New
    for i in range(0, page):  # 页码
        start_num = i*25
        url = base_url.replace("[page]", str(i)).replace('[start]',str(start_num))
        print (url)
        # time.sleep(2)
        html = get_html.get_html(url)

        url_list_re = re.findall(r'<td colspan="2">(.*?)</td>', html, re.S)
        print (url_list_re)
        url_list = re.findall(r'<A HREF="(.*?)">',str(url_list_re),re.S)
        print (url_list)

        print (len(url_list))
        for goods_url in url_list:
            with open("./Result/items_url.txt", "aw") as f:
                f.write('http://www.frys.com/'+goods_url + "\n")
                print (goods_url)

if __name__ == "__main__":
    url = '''http://www.frys.com/search?cat=-68332&pType=pDisplay&resultpage=[page]&start=[start]&rows=25'''
    page = 5
    file_name = './Result/tablets.xls'
    get_asin(url, page)
    # start('./Result/items_url.txt',file_name)
