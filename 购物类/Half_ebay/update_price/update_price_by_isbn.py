# import time
# import datetime
# import random
# import urllib2
# import re
# import StringIO
# import gzip
# import os
# from multiprocessing import Pool, Lock
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import smtplib
# import time
# import logging
# import logging.config
#
# logging.config.fileConfig("/home/ytroot/桌面/WorkSpaceLHW/Half.ebay/log/logging.conf")  # 采用配置文件
# logger1 = logging.getLogger("logger1")
# logger2 = logging.getLogger("logger2")
#
# url = "http://search.half.ebay.com/[isbn]_W0QQmZbooksQQ_trksidZp2919Q2em1447Q2el2686"  # "http://search.half.ebay.com/[isbn]_W0QQmZbooks"
#
# def get_list_random(list_value):
#     """
#     :param list_value:原数组
#     :return:数组的一个随机值
#     """
#     temp_index = random.randint(0, len(list_value) - 1)
#     return list_value[temp_index]
#
#
# '''
#     获取网页的源代码
# '''
# def get_html(url):
#     headers = {'User-Agent': [
#         "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/ Safari/530.5",
#         "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-US) AppleWebKit/530.6 (KHTML, like Gecko) Chrome/ Safari/530.6",
#         "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-US) AppleWebKit/530.9 (KHTML, like Gecko) Chrome/ Safari/530.9",
#         "Mozilla/5.0 (Macintosh; U; Mac OS X 10_5_7; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/ Safari/530.5",
#         "Mozilla/5.0 (Macintosh; U; Mac OS X 10_6_1; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/ Safari/530.5",
#         "Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13(KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.0; de) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.30 Safari/525.13",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.30 Safari/525.13",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.6 Safari/525.13",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.6 Safari/525.13",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.151.0 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.151.0 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.151.0 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.152.0 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.152.0 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.153.0 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.153.0 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.153.1 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.3.154.6 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.3.154.9 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.3.155.0 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/528.4 (KHTML, like Gecko) Chrome/0.3.155.0 Safari/528.4",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.4.154.18 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.4.154.31 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.39 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.42 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.43 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.43 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.43 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.43 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.46 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.48 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.50 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.50 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19"
#
#     ]}
#     try:
#         headers['User-Agent'] = get_list_random(headers['User-Agent'])
#         req = urllib2.Request(url, headers=headers)
#         resp = urllib2.urlopen(req, timeout=10)
#         html = resp.read()
#         return html
#     except Exception as e:
#         print 'error:', str(e)
#         logger2.error(str(e))
#         get_html(url)
#
#
# '''
# url：http://search.half.ebay.com/[isbn]_W0QQmZbooks
#     获取书籍信息
# '''
# def get_book_info(isbn):
#     url = "http://search.half.ebay.com/" + isbn.replace("\n", "") + "_W0QQmZbooksQQ_trksidZp2919Q2em1447Q2el2686"
#     print url
#     time.sleep(2.5)
#     html = get_html(url)
#     if html and -1 == html.find("No products found for"):
#         if -1 == html.find("Security Measure"):
#             try:
#                 isbn13 = ''
#                 isbn = re.findall('ISBN-10:</b>\s+<span class=""><a href=.*? class="pdplinks">(.*?)</a>', html)
#                 if isbn:
#                     isbn = isbn[0]
#                 else:
#                     isbn = ''
#                 isbn_13 = re.findall('ISBN-13:</b>\s+<span class=""><a href=.*? class="pdplinks">(.*?)</a>', html)
#                 if isbn_13:
#                     isbn13 = isbn_13[0]
#                 results = re.findall(
#                     '<h2 class="PDP_itemConditionTitle">(.*?)</h2>.*?<table cellpadding="0" cellspacing="0" class="PDP_itemList">(.*?)</table>',
#                     html, re.S)
#                 if results:
#                     condition = {"Brand New": "11",
#                                  "Like New": "1",
#                                  "Very Good": "2",
#                                  "Good": "3",
#                                  "Acceptable": "4"}
#                     for i in xrange(len(results)):
#                         book_info = []
#                         shelf_info = []  # 上架信息
#
#                         book_info.append(isbn)
#                         book_info.append(isbn13)
#                         book_info.append(results[i][0])
#
#                         # 上架SKU
#                         sku = isbn + "_" + condition[results[i][0]] + "_SF_MM"
#                         shelf_info.append(sku)
#                         # 对店铺做排除
#                         prices = re.findall(
#                             '<td><span class="PDP_itemPrice">(.*?)</span></td>.*?<td><a class="PDP_sellerName" href=".*?">(.*?)</a></td>',
#                             str(results[i]), re.S)
#                         exclude_seller = ['alibris_books_01', 'alibris_books_02', 'alibris_books_03',
#                                           'alibris_books_04', 'alibris_books_05',
#                                           'alibris_books_06', 'alibris_books_07', 'alibris_books_08',
#                                           'alibris_books_09', 'alibris', 'alibris_movies']
#                         if len(prices) == 1:  # condition下只有一个价格
#                             if prices[0][1] not in exclude_seller:
#                                 book_info.append(prices[0][0])
#                                 # 上架价格
#                                 p1 = (float(prices[0][0].replace("$", "")) + 3.99) * 1.5
#                                 p2 = float(prices[0][0].replace("$", "")) + 13.99
#
#                                 price = str(p1 > p2 and p1 or p2)
#                                 shelf_info.append(price)
#                                 shelf_info.append(price)
#                                 shelf_info.append("8888800")
#                                 shelf_info.append("1")
#                                 shelf_info.append("5")
#
#                             else:
#                                 break
#                         elif len(prices) == 2:  # conditon下有两个价格
#                             count = 0
#                             for i in range(2):
#                                 if prices[i][1] not in exclude_seller:
#                                     book_info.append(prices[i][0])
#                                     orig_price = prices[i][0]  # 记录适合条件的最高价
#                                     count += 1
#                             if count == 0:
#                                 break
#                             else:
#                                 # 上架价格
#                                 p1 = (float(orig_price.replace("$", "")) + 3.99) * 1.5
#                                 p2 = float(orig_price.replace("$", "")) + 13.99
#
#                                 price = str(p1 > p2 and p1 or p2)
#                                 shelf_info.append(price)
#                                 shelf_info.append(price)
#                                 shelf_info.append("8888800")
#                                 shelf_info.append("1")
#                                 shelf_info.append("5")
#
#                         else:
#                             count = 0
#                             for i in range(len(prices)):
#                                 if prices[i][1] not in exclude_seller:
#                                     book_info.append(prices[i][0])
#                                     orig_price = prices[i][0]  # 记录适合条件的最高价
#                                     count += 1
#                                 if count == 2:
#                                     break
#                             if count == 0:
#                                 break
#                             else:
#                                 # 上架价格
#                                 p1 = (float(orig_price.replace("$", "")) + 3.99) * 1.5
#                                 p2 = float(orig_price.replace("$", "")) + 13.99
#
#                                 price = str(p1 > p2 and p1 or p2)
#                                 shelf_info.append(price)
#                                 shelf_info.append(price)
#                                 shelf_info.append("8888800")
#                                 shelf_info.append("1")
#                                 shelf_info.append("5")
#                                 #                         #对店铺不做排除
#                                 #                         prices=re.findall('<td><span class="PDP_itemPrice">(.*?)</span></td>.*?<td><span class="PDP_itemPrice">(.*?)</span></td>',str(results[i]),re.S)
#                                 #                         if prices:
#                                 #                             book_info.append(prices[0][0])
#                                 #                             book_info.append(prices[0][1])
#                                 #                         else:
#                                 #                             prices=re.findall('<td><span class="PDP_itemPrice">(.*?)</span></td>',str(results[i]),re.S)
#                                 #                             if prices:
#                                 #                                 book_info.append(prices[0])
#                                 #                                 book_info.append('')
#
#                         lock.acquire()
#                         result_file.write("\t".join(book_info) + "\n")
#                         result_file.flush()
#                         onshelf_file.write("\t".join(shelf_info) + "\n")
#                         onshelf_file.flush()
#                         lock.release()
#                     print "success:", isbn
#                     lock.acquire()
#                     success_isbn_file.write(isbn + "\n")
#                     success_isbn_file.flush()
#                     lock.release()
#                 else:
#                     print "offshelf:", isbn
#                     lock.acquire()
#                     offshelf_isbn_file.write(isbn + "\n")
#                     offshelf_isbn_file.flush()
#                     lock.release()
#             except BaseException, e:
#                 print isbn, e
#                 logger2.exception(str(e))
#         else:
#             lock.acquire()
#             not_crawl_file.write(isbn)
#             not_crawl_file.flush()
#             lock.release()
#     else:
#         lock.acquire()
#         not_list_file.write(isbn + "\n")
#         not_list_file.flush()
#         lock.release()
#
#
# def create_titles(filename, titles):
#     f = open(filename, "w")
#     f.write("\t".join(titles) + "\n")
#     f.flush()
#     f.close()
#
#
# '''
# # info_file = "./update/info/half_info.csv"
# # shelf_file = "./update/info/onshelf_info.csv"
# # isbnfile = "./update/isbn/isbns.csv"
# '''
#
# def update_book_info(isbnfile, shelf_file, info_file):
#     '''根据isbn更新half.com价格'''
#     global result_file  # 结果文件
#     global onshelf_file  # 上架信息结果文件
#     global success_isbn_file
#     global offshelf_isbn_file
#     global not_crawl_file
#     global not_list_file
#     global lock
#     lock = Lock()
#
#     result_file = open(info_file, "w")
#     onshelf_file = open(shelf_file, "w")
#     success_isbn_file = open("./update/info/success_isbn.txt", "w")
#     offshelf_isbn_file = open("./update/info/offshelf_isbn.txt", "w")
#     not_crawl_file = open("./update/info/not_crawl.txt", "w")
#     not_list_file = open("./update/info/not_found.txt", "w")
#
#     titles = ['ISBN', 'ISBN13', 'condition', 'price', 'sec_price']
#     shelf_titles = ['sku', 'price', 'minimum-seller-allowed-price', 'maximum-seller-allowed-price', 'quantity',
#                     'leadtime-to-ship']
#     create_titles(info_file, titles)
#     create_titles(shelf_file, shelf_titles)
#     # 取isbn列表
#     isbn_file = open(isbnfile)
#     isbns = isbn_file.readlines()
#
#     pool = Pool(20)
#     pool.map(get_book_info, isbns)
#     pool.close()
#     pool.join()
#
#     result_file.close()
#     onshelf_file.close()
#     success_isbn_file.close()
#     not_list_file.close()
#     not_crawl_file.close()
#
#
# def send_email(infofile, onshelf_file):
#     # 创建一个带附件的实例
#     msg = MIMEMultipart()
#     # 构造附件1
#     att1 = MIMEText(open(infofile, 'rb').read(), 'base64', 'utf-8')
#     att1["Content-Type"] = 'application/octet-stream'
#     att1["Content-Disposition"] = 'attachment; filename="half_info.csv"'  # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
#     msg.attach(att1)
#     # 构造附件2
#     att2 = MIMEText(open(onshelf_file, 'rb').read(), 'base64', 'utf-8')
#     att2["Content-Type"] = 'application/octet-stream'
#     att2["Content-Disposition"] = 'attachment; filename="onshelf_info.csv"'  # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
#     msg.attach(att2)
#     # 加邮件头
#     # to_list=['liz0505@starmerx.com','lujuan@starmerx.com','lily@starmerx.com','jiping@starmerx.com']#发送给相关人员
#     # to_list = ['3394722605@qq.com', 'miaomiao@starmerx.com', 'zhaolei@starmerx.com']
#     to_list = ['695229425@qq.com'] #测试
#
#     msg['to'] = ';'.join(to_list)
#     msg['from'] = 'hengwei@starmerx.com'
#     msg['subject'] = 'half.com价格自动更新'
#     # 发送邮件
#     try:
#         server = smtplib.SMTP()
#         server.connect('smtp.exmail.qq.com')
#         server.login('hengwei@starmerx.com', 'Lianyu2016')  # XXX为用户名，XXXXX为密码
#         server.sendmail(msg['from'], to_list, msg.as_string())
#         print '发送成功', infofile
#     except Exception, e:
#         print '发送失败', e
#         logger2.error(str(e))
#         server.quit()
#         send_email(infofile)
#     finally:
#         server.quit()
#
#
# if __name__ == "__main__":
#     try:
#         t1 = datetime.datetime.now()
#         logger1.info('start:update_book_info()')
#         info_file = "./update_price/goods_info/half_info.csv"
#         shelf_file = "./update_price/goods_info/onshelf_info.csv"
#         isbnfile = "./update_price/isbn_Data/isbns.csv"
#         update_book_info(isbnfile, shelf_file, info_file)
#         send_email(info_file, shelf_file)
#         logger1.info('over:update_book_info()')
#         t2 = datetime.datetime.now()
#         print '开始时间：', t1
#         print '结束时间：', t2
#     except Exception, e:
#         print e
#         logger2.error(str(e))
#
# # html = get_html('http://search.half.ebay.com/9781932173970_W0QQ_trksidZp2919Q2em1447Q2el2686QQmZbooks')
# #     if html and -1==html.find("No products found for"):
# #         with open('aa.html','w') as f:
# #            f.write(html)
# #            print '-----888'*2,html.find("No products found for")
# #     else:
# #         print 'true'
#
#

import re
import requests
url="http://search.half.ebay.com/0803966156_W0QQmZbooksQQ_trksidZp2919Q2em1447Q2el2686"
req = requests.get(url)
html = req.text
results = re.findall('<h2 class="PDP_itemConditionTitle">(.*?)</h2>.*?<table cellpadding="0" cellspacing="0" class="PDP_itemList">(.*?)</table>',html,re.S)

print (results)
print (len(results))