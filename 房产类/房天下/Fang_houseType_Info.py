import requests
from bs4 import BeautifulSoup
import random
import pymysql
from multiprocessing import Pool,Lock
import re
import urllib.request
# from random import choice

def get_proxies_ip():
    db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    # db = pymysql.connect("192.168.1.231","root","3jw9lketj0","ConstructionMaterials",charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM proxies_info;"
    proxies_list = []
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            proxy_ip = row[1]
            proxy_port = str(row[2])
            proxies_list.append(proxy_ip+':'+proxy_port)
    except:
        db.rollback()
    db.close()
    proxies_info = {
        'http':'http://'+random.choice(proxies_list)
    }
    return proxies_info

def get_headers():
    USER_AGENTS = ['Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
           'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
           'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
           'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
           'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
           'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
           'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1']

    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # 'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Host':'m.fang.com',
    }

def makeMyOpener():
    headers = get_headers()
    proxies_list = get_proxies_ip()
    # cj = http.cookiejar.CookieJar() # urllib.request.HTTPCookieProcessor(cj)
    proxy_support = urllib.request.ProxyHandler({'http':"http://"+random.choice(proxies_list)})
    opener = urllib.request.build_opener(proxy_support,urllib.request.HTTPHandler)
    header = []
    for key, value in headers.items():
        elem = (key, value)
        header.append(elem)
    opener.add_headers = header

    urllib.request.install_opener(opener)
    return opener

# ''http://www.fang.com/house/1010122849/housedetail.htm''
def get_house_type(code_tuple):
    # print(code_tuple)
    city_name = code_tuple[0]
    city_newcode = code_tuple[1]
    house_name = code_tuple[2]
    city_code = code_tuple[3]
    'http://m.fang.com/xiaoqu/lz/3711244006/photo_huxingimg.html'
    basic_info_url = 'http://m.fang.com/xf.d?m=huXingList&city={cityCode}&newcode={houseCode}'.format(cityCode=city_code,houseCode=city_newcode)
    house_detail_url = 'http://www.fang.com/house/{}/housedetail.htm'.format(city_newcode)
    try:
        data_request = requests.get(basic_info_url,headers=get_headers(),proxies=get_proxies_ip(),timeout=30)
        data_request.encoding = 'gbk'
        html_info = data_request.text
        # print(basic_info_url)
        soup = BeautifulSoup(html_info,'html.parser')
        info_list = soup.select('article#room ul li a')
        try:
            # house_name_re = re.findall("<title>(.*?)</title>",html_info)
            # house_name = house_name_re[0].split('户型图')[0].strip('【')
            for info in info_list:
                house_image = 'http:'+info.div.img['src']
                house_basic = info.h2.text
                house_type = house_basic.split('\xa0')[0]
                house_area = house_basic.split('\xa0')[1]
                try:
                    house_price = info.i.text
                except:
                    house_price = info.strong.text.strip()

                house_info = info.p.text
                house_key = info.span.text
                lock.acquire()
                # print(house_name+'\t'+house_image+'\t'+house_info+'\t'+house_type+'\t'+house_area+'\t'+house_price+'\t'+house_key+'\n')
                house_type_file.write(city_name+'\t'+house_name+'\t'+house_image+'\t'+house_info+'\t'+house_type+'\t'+house_area+'\t'+house_price+'\t'+house_key+'\t'+house_detail_url+'\n')
                house_type_file.flush()
                lock.release()
                print(house_name)
        except Exception as e:
            lock.acquire()
            none_house_info.write(city_name+'\t'+house_name+'\t'+city_code+'\t'+'\n')
            none_house_info.flush()
            lock.release()
            print('for error',e,basic_info_url)
    except Exception as e:
        lock.acquire()
        fail_house_file.write(city_name+'\t'+city_newcode+'\t'+house_name+'\t'+city_code+'\n')
        fail_house_file.flush()
        lock.release()
        print('requests error ',e)

def send_code():
    global lock,house_type_file,fail_house_file,none_house_info
    lock = Lock()
    city_info = []
    house_type_file = open('./data/fang_house_type.csv','w')
    fail_house_file = open('./data/fang_fail_house_type.csv','w')
    none_house_info = open('./data/fang_none_house.csv','w')
    with open('./data/fang_city_url.csv','r') as city_url_file:
        for city_info_list in city_url_file.readlines():
            city_name = city_info_list.split('\t')[0]
            city_newcode = city_info_list.split('\t')[3]
            house_name = city_info_list.split('\t')[4].strip()
            city_code = city_info_list.split('\t')[5].strip()

            city_tuple = (city_name,city_newcode,house_name,city_code)
            city_info.append(city_tuple)

    titles = ['城市名','楼盘名','户型图','户型名称','厅室数目','房屋面积','房屋售价','销售状态','楼盘详情地址']
    house_type_file.write('\t'.join(titles)+'\n')
    house_type_file.flush()

    pool = Pool(20)
    pool.map(get_house_type,city_info)
    pool.close()
    pool.join()

    house_type_file.close()
    fail_house_file.close()
    none_house_info.close()

# def deal_fail_info():
#     global lock,house_type_file,fail_house_file,none_house_info
#     lock = Lock()
#     city_info = []
#     import os
#     os.system('sort -u ' + './data/fang_fail_house_type.csv' + ' > ' + './data/fang_new_house.csv')
#
#     house_type_file = open('./data/fang_house_type_xu.csv','w')
#     fail_house_file = open('./data/fang_fail_house_type.csv','w')
#     none_house_info = open('./data/fang_none_house.csv','w')
#
#     with open('./data/fang_new_house.csv','r') as city_url_file:
#         for city_info_list in city_url_file.readlines():
#             city_name = city_info_list.split('\t')[0]
#             city_newcode = city_info_list.split('\t')[1]
#             city_city = city_info_list.split('\t')[2].strip()
#             city_tuple = (city_name,city_newcode,city_city)
#             city_info.append(city_tuple)
#
#     titles = ['城市名','楼盘名','户型图','户型名称','厅室数目','房屋面积','房屋售价','销售状态','楼盘详情地址']
#     house_type_file.write('\t'.join(titles)+'\n')
#     house_type_file.flush()
#
#     pool = Pool(20)
#     pool.map(get_house_type,city_info)
#     pool.close()
#     pool.join()
#     house_type_file.close()
#     fail_house_file.close()
#     none_house_info.close()

if __name__ == '__main__':
    send_code()
    # deal_fail_info()