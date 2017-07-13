import time
import random
import os
from Tools import get_html
from multiprocessing import Pool, Lock
import re


# def get_count(price_range, url):  # 没有解析出count的url记录下来。
#     try:
#         html = get_html.get_html_src(url)
#         if html == '' or -1 != html.find('Sorry, we just need to make sure you'):
#             lock.acquire()
#             captcha_url_file.write(url + '\n')
#             captcha_url_file.flush()
#             lock.release()
#             return
#         if html == '404 error':
#             lock.acquire()
#             not_list_file.write(url + '\n')
#             not_list_file.flush()
#             lock.release()
#             # print 'product not found'
#             return
#         # 没有抓下来的页面
#         if html == 'time out or other errors':
#             lock.acquire()
#             not_crawl_file.write(price_range + '\n')
#             not_crawl_file.flush()
#             lock.release()
#             return
#         num = re.search('<h2 id="s-result-count".*?>1-60 of (.*?) result', html)
#         if num == None:
#             num = re.search('<h2 id="s-result-count".*?>(.*?) result', html)
#
#         if num != None:
#             num = int(num.group(1).replace(',', ''))
#             return num
#         else:
#             if 'did not match any products.' in html:
#                 lock.acquire()
#                 f_no_product.write(url + '\n')
#                 f_no_product.flush()
#                 lock.release()
#             else:
#                 with open('get_count_fail.txt', 'aw') as f:
#                     f.write(price_range + '\n')
#             return
#     except Exception, e:
#         print str(e)

# def get_price_url(high_price):
#     global f_price_url, f_no_product, captcha_url_file, not_list_file, not_crawl_file, lock
#     lock = Lock()
#
#     number = high_price / 50 + 1
#     # print number
#     price_ranges = []
#     for i in range(number):
#         low = i * 50
#         high = (i + 1) * 50
#         price_range = str(low) + '-' + str(high)
#         price_ranges.append(price_range)
#         # print price_range
#     # print price_ranges
#
#     f_price_url = open('./result/price_url.txt', 'w')
#     f_no_product = open('./result/no_product.txt', 'w')
#     captcha_url_file = open('./result/captcha_url.txt', 'w')
#     not_list_file = open('./result/not_found.txt', 'w')
#     not_crawl_file = open('./result/not_crawl.txt', 'w')
#
#     pool = Pool(30)
#     pool.map(handle_url, price_ranges)
#     pool.close()
#     pool.join()
#
#     f_price_url.close()
#     f_no_product.close()
#     captcha_url_file.close()
#     not_list_file.close()
#     not_crawl_file.close()

def get_asin():
    #Electronics : Computers & Accessories : Monitors : Prime Eligible : New

    base_url = '''https://www.amazon.com/s/ref=sr_pg_[i]?fst=as%3Aoff&rh=n%3A172282%2Cn%3A!493964%2Cn%3A172541%2Cn%3A12097478011%2Cp_85%3A2470955011%2Cp_n_condition-type%3A2224371011&page=[i]&bbn=12097478011&ie=UTF8&qid=1479085629'''
    for i in range(1, 222):  # 页码，共2页
        url = base_url.replace("[i]", str(i))
        print (url)
        time.sleep(2)
        html = get_html.get_html(url)

        url_list = re.findall(r'<a class="a-link-normal s-access-detail-page .*? href="(.*?)">', html, re.S)
        print (len(url_list))

        for goods_url in url_list:
            with open("./Result/items_url.txt", "aw") as f:
                f.write(goods_url + "\n")
                print (goods_url)
            items_asin = re.findall(r'/dp/(.*?)/ref',goods_url,re.S)
            # for item_asin in items_asin:
            #     with open("./Result/items_asin.txt",'aw') as asin:
            #         asin.write(item_asin+'\n')
            #         print item_asin


if __name__ == "__main__":
    get_asin()
