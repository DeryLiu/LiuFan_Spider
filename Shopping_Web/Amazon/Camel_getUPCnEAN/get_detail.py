from Tools import ALL_CONFIG
import re
import time
from multiprocessing import Pool, Lock
import requests

def create_titles():
    f = open(ALL_CONFIG.CAMEL_UPCEAN_FILE,"w")
    titles = ['asin','upc','ean']
    f.write("\t".join(titles)+"\n")
    f.flush()
    f.close()

def send_asin():
    global info_file
    info_file = open(ALL_CONFIG.CAMEL_UPCEAN_FILE, 'a')

    for asins in open(ALL_CONFIG.CAMEL_UPCEAN_ASIN,'r').readlines():
        # time.sleep(2)
        get_product_url(asins)
    # lock = Lock()

    # pool = Pool(10)
    # pool.map(get_product_url,asin_list)
    # pool.close()
    # pool.join()
    #
    # info_file.close()


def get_product_url(asin):
    # headers = {
    #     'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
    #     'Referer':'http://camelcamelcamel.com/Thing-Explainer-Complicated-Stuff-Simple/product/0544668251',
    #     'Host':'camelcamelcamel.com',
    #     'Connection':'keep-alive',
    #     'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    #     'Accept-Encoding':'gzip, deflate',
    #     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    # }
    # url_product = 'http://camelcamelcamel.com/product/'+ asin
    url_search = 'http://camelcamelcamel.com/search?sq='+asin
    try:
        # info_r = requests.get(url_product,headers=headers,timeout=20)
        info_r = requests.get(url_search)
        print (info_r.url)
        # print info_r.status_code
        detail_url = info_r.url + '?active=details'
        get_datail_info(detail_url)
    except Exception as e:
        print (url_search,e)


def get_datail_info(url):
    asin = re.findall('product/(.*?)active=details',url,re.S)
    asin = str(asin).replace("?","").replace("[u'","").replace("']","")
    info_list = []
    info_list.append(asin)
    detail_r = requests.get(url,timeout=10)
    detail_html = detail_r.text
    info_all = re.findall(r'<meta name="keywords" content="Title:(.*?)/>',detail_html,re.S)
    # print info_all
    try:
        upc_aa = str(info_all).split('UPC:')[1]
        upc = upc_aa.split(',')[0]
    except:
        upc = 'None'
    info_list.append(upc.strip())

    try:
        ean_aa = str(info_all).split('EAN:')[1]
        ean = ean_aa.split(',')[0]
    except:
        ean = 'None'
    info_list.append(ean.strip())
    print (info_list)
    # lock.acquire()
    info_file.write('\t'.join(str(i) for i in info_list)+'\n')
    info_file.flush()
    # lock.release()

if __name__ == '__main__':
    create_titles()
    send_asin()
    # get_product_url('1607747308')