import time
import random
import re
import os
from Tools import get_html

# def get_html_src(url):
#     """
#     get page source
#     :param url:
#     :return:
#     """
#     with open("./Data/headers_list.txt") as f:
#         try:
#             header_list = f.readlines()
#         except Exception, e:
#             print str(e)
#     while True:
#         try:
#             header = {"User-Agent": random.choice(header_list).split("\n")[0]}
#             req = urllib2.Request(url, None, header)
#             page = urllib2.urlopen(req, timeout=10)
#             html = page.read()
#             return html
#         except Exception, e:
#             print str(e)


# def get_html_proxy(url):
#     with open("./Data/proxy_list.txt") as f:
#         try:
#             proxy_list = f.readlines()
#
#         except Exception, e:
#             print str(e)
#     with open("./Data/headers_list.txt") as f:
#         try:
#             header_list = f.readlines()
#             # ASIN = asin.split("\n")[0]
#             # header = "User-Agent:" + random.choice(header_list)
#
#         except Exception, e:
#             print str(e)
#     # header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
#     #                         "(KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36"}
#     # while True:
#     try:
#         proxy = {'http': 'http://' + random.choice(proxy_list).split("\n")[0]}
#         header = {"User-Agent": random.choice(header_list).split("\n")[0]}
#         proxy_support = urllib2.ProxyHandler(proxy)
#         opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
#         urllib2.install_opener(opener)
#         req = urllib2.Request(url, None, header)
#         res = urllib2.urlopen(req, timeout=10)
#         html = res.read()
#         return html
#     except Exception, e:
#         print str(e)

def get_id():
    #Best-BuyCameras & CamcordersCamcordersAction-Camcorders-Action Camcorders
    # http://www.bestbuy.com/site/ipad-tablets-ereaders/tablets/pcmcat209000050008.c?id = pcmcat209000050008

    # base_url = '''http://www.bestbuy.com/site/searchpage.jsp?cp=[i]&searchType=search&browsedCategory=abcat0701000&id=pcat17071&nrp=24&qp=condition_facet%3DCondition~New&sc=Global&searchVariant=A&st=categoryid%24abcat0701000&type=page&usc=All%20Categories'''
    base_url = '''http://www.bestbuy.com/site/searchpage.jsp?cp=[i]&searchType=search&_dyncharset=UTF-8&ks=960&sc=Global&list=y&usc=All%20Categories&type=page&id=pcat17071&iht=n&seeAll=&browsedCategory=pcmcat321000050004&st=categoryid%24pcmcat321000050004&qp=condition_facet%3DCondition~New'''
    # # 只有一页的时候
    # html = get_html.get_html_src(base_url)
    # id_list = re.findall(r'data-sku-id="(.*?)"', html, re.S)
    # print len(id_list)
    # for goods_id in id_list:
    #     with open("./id.txt", "aw") as f:
    #         f.write(goods_id + "\n")
    #         print goods_id

    for i in range(1, 9):  # 页码，共2页
        url = base_url.replace("[i]", str(i))
        print (url)
      #  time.sleep(5)
        html = get_html.get_html_src(url)

        id_list = re.findall(r'data-sku-id="(.*?)"', html, re.S)
        print (len(id_list))
        for goods_id in id_list:
            with open("./id.txt", "aw") as f:
                f.write(goods_id + "\n")
                print (goods_id)

        # with open("./Data/html/" + str(i) + ".html", "aw") as fff:
        #     try:
        #         fff.write(html)
        #     except Exception, e:
        #         print str(e)
        # print "succeed"

# def get_id():
#     for i in range(1, 19):
#         # print i
#         page = open("./Data/All_Laptops/" + str(i) + ".html", "r")
#         html = page.read()
#         id_list = re.findall(r'data-sku-id="(.*?)"', html, re.S)
#         for goods_id in id_list:
#             with open("./Data/id.txt", "aw") as f:
#                 f.write(goods_id + "\n")
#                 print goods_id

#
# def get_info():
#
#     file_id = open("./Data/Id_last.txt", "r")
#     Ids = file_id.readlines()
#     for id in Ids:
#         Id = id.split("\n")[0]
#         print Id
#         url = 'http://www.bestbuy.com/site/products/' + str(Id) + '.p'
#         # print url
#         # time.sleep(5)
#         html = get_html_src(url)
#         if html:
#             with open("./Data/All_Laptops/" + str(Id) + ".html", "aw") as fff:
#                 try:
#                     fff.write(html)
#                 except Exception, e:
#                     print str(e)
#             print "succeed"

if __name__ == "__main__":
    # get_id()
    # # get_items_id()
    # os.system('sort -u ' + './Data/id.txt' + ' > ' + './Data/Id_last.txt')
    # get_info()
    get_id()
    os.system('sort -u ' + './id.txt' + ' > ' + './Id_last.txt')
