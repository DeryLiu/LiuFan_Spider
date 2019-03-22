import requests
import simplejson
import urllib.request
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool,Lock
import time
from random import choice
import pymysql
import random
import http.cookiejar
from io import BytesIO
import gzip

def ungzip(content):
    content = BytesIO(content)
    gzipper = gzip.GzipFile(fileobj=content)
    html = gzipper.read()
    return html

def get_proxies_ip():
    # MAX_RETRIES = 20
    # session = requests.Session()
    # adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
    # session.mount('https://', adapter)
    # session.mount('http://', adapter)
    # rp = session.get(url)
    # db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    db = pymysql.connect("192.168.1.231","root","3jw9lketj0","ConstructionMaterials",charset='utf8')
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
    return proxies_list

def get_headers():
    USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # 'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
    }

def makeMyOpener():
    headers = get_headers()
    proxies_list = get_proxies_ip()
    # cj = http.cookiejar.CookieJar() # urllib.request.HTTPCookieProcessor(cj)
    proxy_support = urllib.request.ProxyHandler({'http':"http://"+choice(proxies_list)})
    opener = urllib.request.build_opener(proxy_support,urllib.request.HTTPHandler)
    header = []
    for key, value in headers.items():
        elem = (key, value)
        header.append(elem)
    opener.add_headers = header

    urllib.request.install_opener(opener)
    return opener

# 1.获取城市code
def get_city_code():
    # 获得城市的list
    city_list = []
    with open('./data/cm_city.csv','r') as city_file:
        for city_info in city_file.readlines():
            city_list.append([city.strip('",\n') for city in city_info.split(',')])
        # print(city_list)

    url = 'http://newhouse.fang.com/house/s/#?ctm=1.bj.xf_search.head.2'
    # handle()
    # start(url)
    re_re = requests.get(url)
    re_re.encoding = 'gb2312'
    soup = BeautifulSoup(re_re.text,'html.parser')
    city_info_list = soup.select('div.city20141104 div.city20141104nr a')
    print(len(city_info_list))
    with open('./data/fang_city_list.csv','w') as city_file:
        for city_a in city_info_list:
            for city_name in city_list:
                if city_a.text in city_name[2]:
                    # print(city_a.text+'\t'+city_name[1]+'\t'+city_name[0]+'\t'+city_a['href']+'\n')
                    city_file.write(city_a.text+'\t'+city_name[1]+'\t'+city_name[0]+'\t'+city_a['href']+'\n')

# 2.获取url
def get_city_url(info_list):
    try:
        city_name_cn = info_list[0].strip()
        city_province_id = info_list[1].strip()
        city_city_id = info_list[2].strip()
        city_city_url = info_list[3].strip()
        # print(city_name_cn,city_province_id,city_city_id,city_city_url)
        page_num_request = requests.get(city_city_url)
        page_num_request.encoding = 'gb2312'
        page_num = BeautifulSoup(page_num_request.text,'html.parser').select('#sjina_C01_47 > ul > li.fr > a')[-1]['href'].split('b9')[1].strip('/')
        print(city_name_cn,page_num)
        city_url_code = city_city_url.split('.')[1]
        if city_url_code == 'fang':
            city_url_code = 'bj'
        url_list = [(city_city_url+'b9{page}/?ctm=1.{city_code}.xf_search.page.{page}').format(page =i+1,city_code=city_url_code) for i in range(int(page_num))]
        # print(url_list)
        for url in url_list:
            # time.sleep(1)
            data_request = requests.get(url)
            data_request.encoding = 'gb2312'
            data_html_info = data_request.text
            soup = BeautifulSoup(data_html_info,'html.parser')
            id_list =  soup.select('div.sslalone')
            for i in id_list:
                house_id = i['id'].split('loupan_')[1]
                house_na = i.a.img['alt']
                lock.acquire()
                detail_url_file.write(city_name_cn+'\t'+city_province_id+'\t'+city_city_id+'\t'+house_id+'\t'+house_na+'\n')
                detail_url_file.flush()
                # print(house_na)
                lock.release()
            # # --------获取url部分------
            # # 链接
            # f_link = soup.select('div .nlcd_name a')['href']
            # print(f_link)
            # # 产品id
            # f_number_eleamt = soup.select('div.notice div.duibi')['onclick']
            # f_number = ''.join(re.findall('[0-9]',f_number_eleamt))
            # # 商品详情
            # if 'www.fang.com' in f_link:
            #     f_link_detail = 'http://www.fang.com/house/'+f_number+'/housedetail.htm'
            # else:
            #     f_link_detail = f_link+'house/'+f_number+'/housedetail.htm'
            # # lock.acquire()
            # # --------获取url部分------
            # with open('./data/fang_city_url.csv','a') as detail_url_file:
            #     for i in id_list:
            #         # print(city_name_cn+'\t'+city_province_id+'\t'+city_city_id+'\t'+i['onclick'].split("'")[1]+'\n')
            #         detail_url_file.write(city_name_cn+'\t'+city_province_id+'\t'+city_city_id+'\t'+i['onclick'].split("'")[1]+'\n')
    except Exception as e:
        print(e)
# 3.主函数
def get_fang_info():
    url_file = open('./data/fang_city_url.csv','r').readlines()
    db = pymysql.connect("192.168.1.231","root","3jw9lketj0","ConstructionMaterials",charset='utf8')
    cursor = db.cursor()
    for url_code in url_file:
        province_id_code = url_code.split('\t')[1].strip()
        city_id_code = url_code.split('\t')[2].strip()
        house_id_code = url_code.split('\t')[3].strip()
        headers = get_headers()
        proxies_ip = random.choice(get_proxies_ip())
        proxies = {
            "http":"http://"+proxies_ip,
            "https":"https://"+proxies_ip,
        }
        # print(proxies)
        # print(headers)
        try:
            time.sleep(1)
            house_basic_url = 'http://www.fang.com/house/{}/housedetail.htm'.format(house_id_code)
            # 法1：
            # try:
                # MAX_RETRIES = 3
                # session = requests.Session()
                # adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
                # session.mount('https://', adapter)
                # session.mount('http://', adapter)
                # data_requests = session.get(house_basic_url,headers=headers,proxies=proxies,timeout=20)
                # data_requests.encoding = 'gb2312'
            # except Exception as e:
            #     print(e)
            # session = requests.session()
            # try:
            #     data_requests = session.get(house_basic_url,headers=headers,proxies=proxies,timeout=20)
            # except Exception as e:
            #     print('requests error ',e)
            # data_requests.encoding = 'gb2312'
            # soup = BeautifulSoup(data_requests.text,'html.parser')

            # # 法2：
            time.sleep(2)
            opr = makeMyOpener()
            # print(house_basic_url)
            uop = opr.open(house_basic_url, timeout = 30)
            # data_requests = gzip.decompress(uop.read()).decode("gb18030")
            data_requests = uop.read().decode('gb18030', 'ignore')
            # data_requests = ungzip(data_requests)
            soup = BeautifulSoup(data_requests,'html.parser')
            salse_status = {
                '待售':1,
                '在售':2,
                '售完':3,
                '出租':2,
                '租售':2,
            }
            # have_demo = {'否':0, '是':1}
            c_f_link = ''
            c_f_name = ''
            c_f_province_id = province_id_code
            c_f_city_id = city_id_code
            c_f_area_id = 0
            # 销售状态
            c_f_salse_status = 2
            # 装修状态
            c_f_redecorate_type = ''
            # 毛胚总户数
            c_f_rough_door_count = 0
            # 精装总户数
            c_f_good_door_count = 0
            # 当期毛胚户数
            c_f_now_rough_door_count = 0
            # 当期精装总户数
            c_f_now_good_door_count = 0
            # 户型及户数
            c_f_brunt = ''
            # 精装标准 元/平米
            c_f_redecorate_price = ''
            # 楼栋总数
            c_f_building_count = 0
            # 楼层状况
            c_f_floor_status = ''
            # 工程进度
            c_f_progress = ''
            # 是否有样板房 0=否 1=是
            c_f_have_demo = 0
            # 样板房配套品牌
            c_f_demo_brand = ''
            # 物业公司
            c_f_property_firm = ''
            # 均价
            c_f_price = ''
            # 详细地址
            c_f_address = ''
            # 环线位置
            c_f_metro_info = ''
            # 开发商
            c_f_developer = ''
            # 总户数
            c_f_door_count = 0
            # 占地面积
            c_f_area_covered = ''
            # 建筑面积
            c_f_built_up  = ''
            # 产权
            c_f_property_right = ''
            # 物业类型
            c_f_property = ''
            # 开盘时间
            c_f_open_time = ''
            # 交房时间
            c_f_others_time = ''
            # 售楼电话
            c_f_salse_telphone = ''
            # 售楼地址
            c_f_salse_address = ''

            if 'xiangqing/' in house_basic_url:
                c_f_link = house_basic_url.replace('xiangqing/','')
                c_f_name = soup.select('h1 a.tt')[0].text
                # 均价
                try:
                    c_f_price = soup.select('div.box dl dd span.red')[0].text
                except:
                    c_f_price = ''

                all_data_list = soup.select('div.con_left div.box dd')
                # print(all_data_list)
                for i in range(len(all_data_list)):
                    # print(all_data_list[i].text)
                    if '物业类别'in all_data_list[i].text:
                        # 物业类型
                        c_f_property = all_data_list[i].text.split('：')[1]
                    if '小区地址' in all_data_list[i].text:
                        # 详细地址
                        c_f_address = all_data_list[i].text.split('：')[1]
                    if '环线位置' in all_data_list[i].text:
                        # 环线位置
                        c_f_metro_info = all_data_list[i].text.split('：')[1]
                    if '开 发 商' in all_data_list[i].text:
                        # 开发商
                        c_f_developer = all_data_list[i].text.split('：')[1]
                    if '产权描述' in all_data_list[i].text:
                        # 产权年限
                        c_f_property_right = all_data_list[i].text.split('：')[1]
                    if '建筑面积' in all_data_list[i].text:
                        # 建筑面积
                        c_f_built_up = all_data_list[i].text.split('：')[1]
                    if '占地面积' in all_data_list[i].text:
                        # 占地面积
                        c_f_area_covered = all_data_list[i].text.split('：')[1]
                    if '物业公司' in all_data_list[i].text:
                        # 物业公司
                        c_f_property_firm = all_data_list[i].text.split('：')[1]
                    if '开盘时间：' in all_data_list[i].text:
                        # 开盘时间
                        c_f_open_time = all_data_list[i].text.split('：')[1]
                    if '交房时间' in all_data_list[i].text:
                        # 交房时间
                        c_f_others_time = all_data_list[i].text.split('：')[1]
                    if '售楼电话' in all_data_list[i].text:
                        # 售楼电话
                        c_f_salse_telphone = all_data_list[i].text.split('：')[1]
                    if '售楼地址' in all_data_list[i].text:
                        # 售楼地址
                        c_f_salse_address = all_data_list[i].text.split('：')[1]
            else:
                c_f_link = house_basic_url.replace('/housedetail','')

                try:
                    try:
                        c_f_name = soup.select('h1 a')[0]['title']
                    except IndexError:
                        c_f_name = soup.select('h1 a')[0].text
                except:
                    c_f_name = ''
                # 均价
                # if soup.select('div.main-info-price')[0].text.split('<em>')[0].split('：')[1].strip():
                try:
                    c_f_price = soup.select('div.main-info-price')[0].text.split('<em>')[0].split('：')[1].strip()
                except:
                    c_f_price = ''

                all_data_list = soup.select('ul li div')
                for i in range(len(all_data_list)):
                    if '物业类别'in all_data_list[i].text:
                        # 物业类型
                        c_f_property = all_data_list[i+1].text.strip()
                    if '楼盘地址' in all_data_list[i].text:
                        # 详细地址
                        c_f_address = all_data_list[i+1].text.strip()
                    if '环线位置' in all_data_list[i].text:
                        # 环线位置
                        c_f_metro_info = all_data_list[i+1].text.strip()
                    if '销售状态' in all_data_list[i].text:
                        # 销售状态
                        c_f_salse_status_value = all_data_list[i+1].text.strip()
                        if c_f_salse_status_value == '':
                            c_f_salse_status_value = '在售'
                        c_f_salse_status=salse_status[c_f_salse_status_value]
                    if '开发 商：' in all_data_list[i].text:
                        # 开发商
                        c_f_developer=all_data_list[i+1].text.strip()
                    if '装修状况' in all_data_list[i].text:
                        # 装修状态
                        c_f_redecorate_type = all_data_list[i+1].text.split('[')[0].strip()
                    if '楼层状况' in all_data_list[i].text:
                        # 楼层状况
                        c_f_floor_status = all_data_list[i+1].text.strip()
                    if '产权年限' in all_data_list[i].text:
                        # 产权年限
                        c_f_property_right = all_data_list[i+1].text.strip()
                    if '建筑面积' in all_data_list[i].text:
                        # 建筑面积
                        c_f_built_up = all_data_list[i+1].text.strip()
                    if '占地面积' in all_data_list[i].text:
                        # 占地面积
                        c_f_area_covered=all_data_list[i+1].text.strip()
                    if '物业公司' in all_data_list[i].text:
                        # 物业公司
                        c_f_property_firm=all_data_list[i+1].text.strip()
                    if '开盘时间：' in all_data_list[i].text:
                        # 开盘时间
                        c_f_open_time = all_data_list[i+1].text.split('[')[0].strip()
                    if '交房时间' in all_data_list[i].text:
                        # 交房时间
                        c_f_others_time=all_data_list[i+1].text.strip()
                    if '售楼电话' in all_data_list[i].text:
                        # 售楼电话
                        c_f_salse_telphone=all_data_list[i+1].text.strip()
                    if '售楼地址' in all_data_list[i].text:
                        # 售楼地址
                        c_f_salse_address=all_data_list[i+1].text.strip()

            with open('./data/cm_area.csv','r') as cm_area_csv_file:
                        for cm_area_items in cm_area_csv_file.readlines():
                            cm_area_item = cm_area_items.split(',')
                            if cm_area_item[2].split('"')[1] in c_f_address:
                                c_f_area_id = cm_area_item[0].split('"')[1]
                                # print(c_f_area_id)
            c_f_record_time = int(time.time())
            c_f_update_time = int(time.time())
            # threadLock.acquire()
            # print(c_f_record_time,c_f_update_time,c_f_link,c_f_name,c_f_province_id,c_f_city_id,c_f_area_id,c_f_address,c_f_metro_info,c_f_salse_status,c_f_developer,c_f_redecorate_type,c_f_door_count,c_f_rough_door_count,c_f_good_door_count,c_f_now_rough_door_count,c_f_now_good_door_count,c_f_brunt,c_f_redecorate_price,c_f_building_count,c_f_floor_status,c_f_progress,c_f_area_covered,c_f_built_up,c_f_property_right,c_f_property,c_f_property_firm,c_f_price,c_f_have_demo,c_f_demo_brand,c_f_open_time,c_f_others_time,c_f_salse_telphone,c_f_salse_address)
            if c_f_name != '':
                try:
                    search_sql = "SELECT * FROM `cm_data_fangcom` WHERE f_link = '{}';".format(c_f_link)
                    # print(search_sql)
                    cursor.execute(search_sql)
                    if len(cursor.fetchall()):
                        # print(res)
                        update_sql = "UPDATE cm_data_fangcom SET f_update_time={},f_link='{}', f_name='{}', f_province_id={}, f_city_id={}, f_area_id={}, f_address='{}', f_metro_info='{}', f_salse_status={}, f_developer='{}', f_redecorate_type='{}', f_door_count={}, f_rough_door_count={}, f_good_door_count={}, f_now_rough_door_count={}, f_now_good_door_count={}, f_brunt='{}', f_redecorate_price='{}', f_building_count={}, f_floor_status='{}', f_progress='{}', f_area_covered='{}', f_built_up='{}', f_property_right='{}', f_property='{}', f_property_firm='{}', f_price='{}', f_have_demo={}, f_demo_brand='{}', f_open_time='{}', f_others_time='{}', f_salse_telphone='{}',f_salse_address='{}' ".format(c_f_update_time,c_f_link,c_f_name,c_f_province_id,c_f_city_id,c_f_area_id,c_f_address,c_f_metro_info,c_f_salse_status,c_f_developer,c_f_redecorate_type,c_f_door_count,c_f_rough_door_count,c_f_good_door_count,c_f_now_rough_door_count,c_f_now_good_door_count,c_f_brunt,c_f_redecorate_price,c_f_building_count,c_f_floor_status,c_f_progress,c_f_area_covered,c_f_built_up,c_f_property_right,c_f_property,c_f_property_firm,c_f_price,c_f_have_demo,c_f_demo_brand,c_f_open_time,c_f_others_time,c_f_salse_telphone,c_f_salse_address)+" WHERE f_name = '{}';".format(c_f_name)
                        # print(update_sql)
                        cursor.execute(update_sql)
                        db.commit()
                        print(c_f_name,'Fang update success')
                    else:
                        insert_sql = "INSERT INTO cm_data_fangcom (f_record_time,f_update_time,f_link, f_name, f_province_id, f_city_id, f_area_id, f_address, f_metro_info, f_salse_status, f_developer, f_redecorate_type, f_door_count, f_rough_door_count, f_good_door_count, f_now_rough_door_count, f_now_good_door_count, f_brunt, f_redecorate_price, f_building_count, f_floor_status, f_progress, f_area_covered, f_built_up, f_property_right, f_property, f_property_firm, f_price, f_have_demo, f_demo_brand, f_open_time, f_others_time, f_salse_telphone,f_salse_address) VALUES ({},{},'{}','{}',{},{},{},'{}','{}',{},'{}','{}',{},{},{},{},{},'{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}');".format(c_f_record_time,c_f_update_time,c_f_link,c_f_name,c_f_province_id,c_f_city_id,c_f_area_id,c_f_address,c_f_metro_info,c_f_salse_status,c_f_developer,c_f_redecorate_type,c_f_door_count,c_f_rough_door_count,c_f_good_door_count,c_f_now_rough_door_count,c_f_now_good_door_count,c_f_brunt,c_f_redecorate_price,c_f_building_count,c_f_floor_status,c_f_progress,c_f_area_covered,c_f_built_up,c_f_property_right,c_f_property,c_f_property_firm,c_f_price,c_f_have_demo,c_f_demo_brand,c_f_open_time,c_f_others_time,c_f_salse_telphone,c_f_salse_address)
                        cursor.execute(insert_sql)
                        db.commit()
                        print(c_f_name,'success commit')

                except Exception as e:
                    print(e)
                    db.rollback()
            else:
                print('楼盘名为空!')
                # print(data_requests)
                print('----------')
            # threadLock.release()
        except Exception as e:
            # print(data_requests.decode())
            print(house_id_code,'error---',e)
    db.close()
# sql = "INSERT INTO cm_data_fangcom (f_record_time,f_update_time,f_link, f_name, f_province_id, f_city_id, f_area_id, f_address, f_metro_info, f_salse_status, f_developer, f_redecorate_type, f_door_count, f_rough_door_count, f_good_door_count, f_now_rough_door_count, f_now_good_door_count, f_brunt, f_redecorate_price, f_building_count, f_floor_status, f_progress, f_area_covered, f_built_up, f_property_right, f_property, f_property_firm, f_price, f_have_demo, f_demo_brand, f_open_time, f_others_time, f_salse_telphone,f_salse_address) VALUES ({},{},'{}','{}',{},{},{},'{}','{}',{},'{}','{}',{},{},{},{},{},'{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}')".format(c_f_record_time,c_f_update_time,c_f_link,c_f_name,c_f_province_id,c_f_city_id,c_f_area_id,c_f_address,c_f_metro_info,c_f_salse_status,c_f_developer,c_f_redecorate_type,c_f_door_count,c_f_rough_door_count,c_f_good_door_count,c_f_now_rough_door_count,c_f_now_good_door_count,c_f_brunt,c_f_redecorate_price,c_f_building_count,c_f_floor_status,c_f_progress,c_f_area_covered,c_f_built_up,c_f_property_right,c_f_property,c_f_property_firm,c_f_price,c_f_have_demo,c_f_demo_brand,c_f_open_time,c_f_others_time,c_f_salse_telphone,c_f_salse_address)+" ON DUPLICATE KEY UPDATE f_record_time={},f_update_time={},f_link='{}', f_name='{}', f_province_id={}, f_city_id={}, f_area_id={}, f_address='{}', f_metro_info='{}', f_salse_status={}, f_developer='{}', f_redecorate_type='{}', f_door_count={}, f_rough_door_count={}, f_good_door_count={}, f_now_rough_door_count={}, f_now_good_door_count={}, f_brunt='{}', f_redecorate_price='{}', f_building_count={}, f_floor_status='{}', f_progress='{}', f_area_covered='{}', f_built_up='{}', f_property_right='{}', f_property='{}', f_property_firm='{}', f_price='{}', f_have_demo={}, f_demo_brand='{}', f_open_time='{}', f_others_time='{}', f_salse_telphone='{}',f_salse_address='{}';" .format(c_f_record_time,c_f_update_time,c_f_link,c_f_name,c_f_province_id,c_f_city_id,c_f_area_id,c_f_address,c_f_metro_info,c_f_salse_status,c_f_developer,c_f_redecorate_type,c_f_door_count,c_f_rough_door_count,c_f_good_door_count,c_f_now_rough_door_count,c_f_now_good_door_count,c_f_brunt,c_f_redecorate_price,c_f_building_count,c_f_floor_status,c_f_progress,c_f_area_covered,c_f_built_up,c_f_property_right,c_f_property,c_f_property_firm,c_f_price,c_f_have_demo,c_f_demo_brand,c_f_open_time,c_f_others_time,c_f_salse_telphone,c_f_salse_address)

def pool_get_city_url():
    global detail_url_file,lock
    lock = Lock()
    detail_url_file =  open('./data/fang_city_url.csv','w')
    city_list_file = open('./data/fang_city_list.csv','r')
    info_list = []
    for city_list_info in city_list_file.readlines():
        city_name_cn = city_list_info.split('\t')[0].strip()
        city_province_id = city_list_info.split('\t')[1].strip()
        city_city_id = city_list_info.split('\t')[2].strip()
        city_city_url = city_list_info.split('\t')[3].strip()
        info_list.append((city_name_cn,city_province_id,city_city_id,city_city_url))

    pool = Pool(10)
    pool.map(get_city_url,info_list)
    pool.close()
    pool.join()
    detail_url_file.close()

if __name__ == '__main__':
    # # 1.获取城市code
    # get_city_code()
    # time.sleep(5)

    # # 2.获取楼盘url
    # pool_get_city_url()
    # time.sleep(5)
    # import os
    # os.system('sort -u ' + './data/fang_city_url1.csv' + ' > ' + './data/fang_city_url.csv')
    # print (time.ctime(time.time()),"Fang 获取楼盘url Finish")

    # # 3.获取实际信息
    get_fang_info()
    print (time.ctime(time.time()),"Fang Finish")
