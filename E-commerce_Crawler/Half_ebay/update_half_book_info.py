import time
import datetime
import random
import requests
import re
from io import StringIO
import os
from multiprocessing import Pool,Lock
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import time
# from get_isbn_from_file import get_isbns
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
    headers = {'User-Agent':[
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

        ]}
    try:
        headers['User-Agent']=get_list_random(headers['User-Agent'])
        req = requests.get(url,headers=headers,timeout=10)
        html = req.text
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
    url = "http://search.half.ebay.com/" + isbn.replace("\n","").strip() + "_W0QQmZbooksQQ_trksidZp2919Q2em1447Q2el2686"
    print (url)
    time.sleep(3.5)
    html = get_html(url)
    if html and -1 == html.find("No products found for"):
        if -1 == html.find("Security Measure"):
            try:
                isbn13 = ''
                isbn = re.findall('ISBN-10:</b>\s+<span class=""><a href=.*? class="pdplinks">(.*?)</a>', html)
                if isbn:
                    isbn = isbn[0]
                else:
                    isbn = ''
                isbn_13 = re.findall('ISBN-13:</b>\s+<span class=""><a href=.*? class="pdplinks">(.*?)</a>', html)
                if isbn_13:
                    isbn13 = isbn_13[0]
                weight = ""
                we = re.findall('Weight:</td><td width="80%" valign="top">(.*?)</td>', html, re.S)
                try:
                    auther_list = re.findall('<span class="pdplinks">(.*?)</span>', html, re.S)
                    auther = str(auther_list).split('class="pdplinks">')[1]
                    auther = auther.split('<')[0]
                    auther.replace("']", '')
                except:
                    auther_list = re.findall(r'<span class="pdplinks">(.*?)</span>', html, re.S)
                    auther = re.findall(r'>(.*?)</a>', str(auther_list), re.S)
                    auther = str(auther).replace("']",'')

                if we:
                    weight = we[0]
                if weight == "":  # 重量为空值，过滤掉
                    # 把所有状态的都取回来，但无效数据太多
                    # for de in fail_condition:
                    #     fail_sku = isbn13 + "_" + de + "_O_MM"  # 美国市场sku
                    #     # fail_sku = off + "EVEN" + isbn + "_"  # 加拿大市场sku
                    #     de_fail = [fail_sku, isbn]
                    #     delete_file.write('\t'.join(de_fail) + '\n')
                    #--------------------------------
                    # 把这些都记录下来，使用不方便
                    delete_file.write(isbn13 + "\n")
                    delete_file.flush()

                else:
                    weight_float = float(weight.replace("oz", "").strip())
                    if weight_float > 60 or weight_float == 0:  # 重量大于60或为0，过滤掉


                        # 把所有状态的都取回来，但无效数据太多
                        # for de in fail_condition:
                        #     fail_sku = isbn13 + "_" + de + "_O_MM"  # 美国市场sku
                        #     # fail_sku = off + "EVEN" + isbn + "_"  # 加拿大市场sku
                        #     de_fail = [fail_sku, isbn]
                        #     delete_file.write('\t'.join(de_fail) + '\n')
                        # -------------------------------
                        delete_file.write(isbn13 + "\n")
                        delete_file.flush()
                    else:
                        results = re.findall(
                            '<h2 class="PDP_itemConditionTitle">(.*?)</h2>.*?<table cellpadding="0" cellspacing="0" class="PDP_itemList">(.*?)</table>',
                            html, re.S)
                        if results:
                            condition = {"Brand New": "11",
                                         "Like New": "1",
                                         "Very Good": "2",
                                         "Good": "3",
                                         "Acceptable": "4"}

                            results_value_list = []
                            condition_list = ['11', '1', '2', '3', '4']
                            condition_fail_dict={'11':'Brand New','1':'Like New','2':'Very Good','3':'Good','4':'Acceptable'}

                            for i in range(len(results)):
                                book_info = []
                                shelf_info = []  # 上架信息

                                book_info.append(isbn)
                                book_info.append(isbn13)
                                book_info.append(weight)
                                book_info.append(auther)
                                book_info.append(results[i][0])

                                # 上架SKU
                                sku = isbn + "_" + condition[results[i][0]] + "_O_MM"  # 美国市场sku
                                # sku=condition[results[i][0]]+"EVEN"+isbn+"_"#加拿大市场sku
                                lock.acquire()
                                success_sku_file.write(sku+'\n')
                                success_sku_file.flush()
                                lock.release()

                                results_value_list.append(condition[results[i][0]])

                                shelf_info.append(sku)
                                # 对店铺做排除
                                prices = re.findall(
                                    '<td><span class="PDP_itemPrice">(.*?)</span></td>.*?<td><a class="PDP_sellerName" href=".*?">(.*?)</a></td>',
                                    str(results[i]), re.S)
                                exclude_seller = ['alibris_books_01', 'alibris_books_02', 'alibris_books_03',
                                                  'alibris_books_04', 'alibris_books_05',
                                                  'alibris_books_06', 'alibris_books_07', 'alibris_books_08',
                                                  'alibris_books_09', 'alibris', 'alibris_movies', 'labsbooks11']
                                price_float = 0.0  # 采购价格

                                if len(prices) == 1:  # condition下只有一个价格
                                    price_float = float(prices[0][0].replace("$", "").replace(",", ""))
                                    if prices[0][1] not in exclude_seller:
                                        book_info.append(prices[0][0])
                                    else:
                                        break
                                elif len(prices) == 2:  # conditon下有两个价格
                                    count = 0
                                    for j in range(2):
                                        if prices[j][1] not in exclude_seller:
                                            book_info.append(prices[j][0])
                                            orig_price = prices[j][0]  # 记录适合条件的最高价
                                            count += 1
                                    if count == 0:
                                        break
                                    else:
                                        # 采购价格
                                        price_float = float(orig_price.replace("$", "").replace(",", ""))

                                else:
                                    count = 0
                                    for j in range(len(prices)):
                                        if prices[j][1] not in exclude_seller:
                                            book_info.append(prices[j][0])
                                            orig_price = prices[j][0]  # 记录适合条件的最高价
                                            count += 1
                                        if count == 2:
                                            break
                                    if count == 0:
                                        break
                                    else:
                                        # 采购价格
                                        price_float = float(orig_price.replace("$", "").replace(",", ""))

                                # 上架价格
                                if price_float > 1:
                                    p1 = (price_float + 3.99) * 1.5
                                    p2 = price_float + 23.99

                                    price = str(p1 > p2 and p1 or p2)  # 美国市场采购价
                                    # price=str(price_float+3.99)#加拿大市场采购价
                                    shelf_info.append(price)
                                    shelf_info.append(price)
                                    # shelf_info.append(auther)
                                    shelf_info.append("8888800")
                                    shelf_info.append("1")
                                    shelf_info.append("5")
                                else:

                                    lock.acquire()
                                    # for de in fail_condition:
                                    #     fail_sku = isbn13 + "_" + de + "_O_MM"  # 美国市场sku
                                    #     # fail_sku = off + "EVEN" + isbn + "_"  # 加拿大市场sku
                                    #     de_fail = [fail_sku, isbn]
                                    #     delete_file.write('\t'.join(de_fail) + '\n')
                                    # delete_file.write("\t".join(book_info) + "\n")
                                    delete_file.flush()
                                    lock.release()
                                    # all_fail_file.write(isbn + '\n')
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

                                result_file.write("\t".join(book_info) + "\n")
                                result_file.flush()

                                onshelf_file.write("\t".join(shelf_info) + "\n")
                                onshelf_file.flush()
                                lock.release()

                            # # 把没有的状态也记录下来
                            # if len(results) < 5:
                            #     last_list = list(set(condition_list) - set(results_value_list))
                            #
                            #     for bu in last_list:
                            #         bu_shelf_info = []
                            #         bu_half_info = []
                            #
                            #         bu_half_info.append(isbn)
                            #         bu_half_info.append(isbn13)
                            #         bu_half_info.append(' ')
                            #         bu_half_info.append(condition_fail_dict[bu])
                            #         bu_half_info.append(' ')
                            #
                            #         # 上架SKU
                            #         sku = isbn + "_" + bu + "_O_MM"  # 美国市场sku
                            #         # sku = condition[results[i][0]] + "EVEN" + isbn + "_"  # 加拿大市场sku
                            #         bu_shelf_info.append(sku)
                            #         bu_shelf_info.append(' ')
                            #         bu_shelf_info.append(' ')
                            #         bu_shelf_info.append(' ')
                            #         bu_shelf_info.append(' ')
                            #         bu_shelf_info.append('5')
                            #
                            #         # for bu_shelf_item in bu_shelf_info:
                            #         lock.acquire()
                            #         bu_half_file.write('\t'.join(bu_half_info)+'\n')
                            #         bu_half_file.flush()
                            #
                            #         bu_onshelf_file.write("\t".join(bu_shelf_info) + "\n")
                            #         bu_onshelf_file.flush()
                            #         lock.release()
                            print ("success:", isbn)
                            lock.acquire()
                            success_isbn_file.write(isbn13 + "\n")
                            success_isbn_file.flush()
                            lock.release()
                        else:
                            print ("offshelf:", isbn)
                            lock.acquire()
                            # for off in fail_condition:
                            #     fail_sku = isbn + "_" + off + "_O_MM"  # 美国市场sku
                            #     # fail_sku = off + "EVEN" + isbn + "_"  # 加拿大市场sku
                            #     all_fail = [fail_sku,'','','','','','0']
                            #     all_fail_file.write('\t'.join(all_fail)+'\n')
                            offshelf_isbn_file.write(isbn13 + "\n")
                            offshelf_isbn_file.flush()
                            lock.release()
                            # all_fail_file.write(isbn+'\n')
            except BaseException as e:
                print (isbn, e)
                logger2.exception(str(e))
        else:
            lock.acquire()
            # for off in fail_condition:
            #     fail_sku = isbn + "_" + off + "_O_MM"  # 美国市场sku
            #     # fail_sku = off + "EVEN" + isbn + "_"  # 加拿大市场sku
            #     all_fail = [fail_sku, '', '', '', '', '', '0']
            #     all_fail_file.write('\t'.join(all_fail) + '\n')
            not_crawl_file.write(isbn)
            not_crawl_file.flush()
            lock.release()
            # all_fail_file.write(isbn+'\n')
    else:
        lock.acquire()
        # for off in fail_condition:
        #     fail_sku = isbn + "_" + off + "_O_MM"  # 美国市场sku
        #     # fail_sku = off + "EVEN" + isbn + "_"  # 加拿大市场sku
        #     all_fail = [fail_sku, '', '', '', '', '', '0']
        #     all_fail_file.write('\t'.join(all_fail) + '\n')
        not_list_file.write(isbn)
        not_list_file.flush()
        lock.release()
        # all_fail_file.write(isbn+'\n')

def create_titles(filename,titles):
    f = open(filename,"w")
    f.write("\t".join(titles)+"\n")
    f.flush()
    f.close()

def update_book_info(isbnfile,shelf_file,info_file):
    '''根据isbn更新half.com价格''' 
    global result_file#结果文件
    global onshelf_file#上架信息结果文件    
    global success_isbn_file
    global offshelf_isbn_file
    global not_crawl_file
    global not_list_file
    # global bu_onshelf_file #condition不符合要求的记录
    # global bu_half_file #----
    global delete_file#记录重量不合条件的ISBN，和采购价低于1的书籍信息
    # global all_fail_file
    global success_sku_file
    global lock
    lock = Lock()
    
    result_file=open(info_file,"w")
    onshelf_file=open(shelf_file,"w")
    # bu_onshelf_file = open('./update/info/onshelf_condition_fail.csv', "w")
    # bu_half_file = open('./update/info/half_condition_fail.csv', "w")
    success_isbn_file=open("./update/info/success_isbn.txt","w")
    offshelf_isbn_file=open("./update/info/offshelf_isbn.txt","w")
    not_crawl_file=open("./update/info/not_crawl.txt","w")
    not_list_file = open("./update/info/not_found.txt","w")
    delete_file=open("./update/info/delete_isbn.txt","w")
    success_sku_file = open("./update/isbn/success_sku.txt",'w')

    # all_fail_file = open("./update/isbn/fail_file.txt",'w')
    
    titles=['ISBN','ISBN13','weight','auther','condition','price','sec_price']
    shelf_titles=['sku','price','minimum-seller-allowed-price','auther','maximum-seller-allowed-price','quantity','leadtime-to-ship']
    create_titles(info_file, titles)
    create_titles(shelf_file, shelf_titles)
    #取isbn列表
#     path="./update/isbn"
#     isbns=get_isbns(path)
    isbn_file = open(isbnfile)
    isbns = isbn_file.readlines()
    #isbns = isbns[:100]
#     #print isbns
    
    pool = Pool(20)
    pool.map(get_book_info,isbns)
    pool.close()
    pool.join()
    
    result_file.close()
    onshelf_file.close()
    success_isbn_file.close()
    success_sku_file.close()
    offshelf_isbn_file.close()
    not_list_file.close()
    # bu_onshelf_file.close()
    # bu_half_file.close()
    not_crawl_file.close()
    delete_file.close()
    # all_fail_file.close()
    
def send_email(infofile):
    # 创建一个带附件的实例
    msg = MIMEMultipart()
    # 构造附件1
    att1 = MIMEText(open(infofile, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="update_info_part8.zip"'#这里的filename可以任意写，写什么名字，邮件中显示什么名字
    msg.attach(att1)
    # 加邮件头
    # to_list=['liz0505@starmerx.com','lujuan@starmerx.com','lily@starmerx.com','jiping@starmerx.com']#发送给相关人员
    to_list=['']
    # to_list=['3394722605@qq.com']
    msg['to'] = ';'.join(to_list)
    msg['from'] = 'user@starmerx.com'
    msg['subject'] = 'half.com价格自动更新 part_8'
    # 发送邮件
    try:
        server = smtplib.SMTP()
        server.connect('smtp.exmail.qq.com')
        server.login('user@starmerx.com','pwd')#XXX为用户名，XXXXX为密码
        server.sendmail(msg['from'], to_list,msg.as_string())
        print ('发送成功',infofile)
    except Exception as e:
        print ('发送失败',e)
        logger2.error(str(e))
        # server.quit()
        send_email(infofile)
    finally:
        server.quit()

def compare_sku():
    success_sku_list = open("./update/isbn/success_sku.txt",'r').readlines()
    all_sku_list = open("./update/isbn/sun_compare.txt",'r').readlines()
    # all_sku_list = open("./update/isbn/even_compare.txt",'r').readlines()

    sku_file = open('./update/info/fail_sku_file.csv','w')
    for i in list(set(all_sku_list) - set(success_sku_list)):
        sku_file.write(i)
    
if __name__=="__main__":
    try:
        t1 = datetime.datetime.now()
        logger1.info('start:update_book_info()')
        info_file="./update/info/half_info.csv"
        shelf_file="./update/info/onshelf_info.csv"
        send_file="update_info.zip"
        isbnfile="./update/isbn/asins_3.csv"
        update_book_info(isbnfile,shelf_file,info_file)
        time.sleep(50)
        compare_sku()
        os.system("zip update_info.zip update/info/*.csv")
        send_email(send_file)
        logger1.info('over:update_book_info()')
        t2 = datetime.datetime.now()
        print ('开始时间：',t1)
        print ('结束时间：',t2)
    except Exception as e:
        print (e)
        logger2.error(str(e))

