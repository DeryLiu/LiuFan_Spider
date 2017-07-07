import requests
import simplejson
from bs4 import BeautifulSoup
import re
import time
from random import choice
import pymysql
import urllib.request
from bs4 import BeautifulSoup
import urllib.error
import threading

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
    proxies_list = ['120.76.79.21:80','120.92.237.69:80','101.4.136.34:81','112.91.135.115:8080', '112.91.135.115:8080']

    proxy_support = urllib.request.ProxyHandler({'http':"http://"+choice(proxies_list)})
    # cj = http.cookiejar.CookieJar() # urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(proxy_support,urllib.request.HTTPHandler)

    # opener = urllib.request.build_opener(urllib.request.HTTPHandler)
    # print('User-Agent',headers['User-Agent'])
    opener.add_headers = [('User-Agent',headers['User-Agent'])]
    urllib.request.install_opener(opener)

    header = []
    for key, value in headers.items():
        elem = (key, value)
        header.append(elem)
    opener.add_headers = header
    return opener

# 1.获取城市的url
def get_focus_city_code():
    # 获得城市的list
    city_list = []
    with open('/root/Spider_Project/data/cm_city.csv','r') as city_file:
        for city_info in city_file.readlines():
            city_list.append([city.strip('",\n') for city in city_info.split(',')])

    url = 'http://sh.focus.cn/search/index.html'

    re_re = requests.get(url)
    soup = BeautifulSoup(re_re.text,'html.parser')
    city_info_list = soup.select('div.bot div div ul li a')
    print(len(city_info_list))
    with open('/root/Spider_Project/data/focus_city_list.csv','w') as city_file:
        for city_a in city_info_list:
            for city_name in city_list:
                if city_a.text in city_name[2]:
                    city_file.write(city_a.text+'\t'+city_name[1]+'\t'+city_name[0]+'\t'+city_a['href']+'\n')

# 2.获取具体的每个城市的楼盘url
def get_url_save(city_list_info):
    city_name_cn = city_list_info.split('\t')[0]
    city_province_id = city_list_info.split('\t')[1]
    city_city_id = city_list_info.split('\t')[2]
    city_city_url = city_list_info.split('\t')[3]
    try:
        # url = 'http://en.wikipedia.org/wiki/Kevin_Bacon'
        headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        html = opener.open(city_city_url)
        num_soup = BeautifulSoup(html, 'html.parser')
        if 'loupan' in city_city_url:
            basic_url = city_city_url.strip()+'p{page_num}/'
            # print(num_request.text)
            # print(num_request.status_code)
            num_select = num_soup.select('div.s-left-menu strong')[0].text
        else:
            basic_url = city_city_url.split('.html')[0]+'_p{page_num}.html'
            num_select = num_soup.select('div.s-left-menu > div.s-m-fr > strong')[0].text
        page_num = int(int(num_select)/20) if int(num_select)%20==0 else int(int(num_select)/20)+1

        url_list = [basic_url.format(page_num=i+1) for i in range(page_num)]

        with open('/root/Spider_Project/data/focus_city_info.csv','a') as detail_url_file:
            # headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')
            # opener = urllib.request.build_opener()
            opener.addheaders = [headers]
            for url_a in url_list:
                ura_html = opener.open(url_a).read().decode('utf8')
                soup = BeautifulSoup(ura_html, 'html.parser')
                # data_request = requests.get(url)
                # soup = BeautifulSoup(data_request.text,'html.parser')
                try:
                    # 链接
                    f_link_list = soup.select('div.s-lp-txt-center > div > a')
                    f_link = [i['href'].replace('.html','/xiangxi/') for i in f_link_list]

                    for j in f_link:
                        # lock.acquire()
                        detail_url_file.write(city_name_cn+'\t'+city_province_id+'\t'+city_city_id+'\t'+j+'\n')
                        # detail_url_file.flush()
                        # lock.release()
                except Exception as e:
                    print(e)

    except urllib.error.HTTPError as reason:
        print(reason)

# 3.抓取所有的楼盘信息，并插入数据库
def get_focus_info():
    db = pymysql.connect("192.168.1.231","root","3jw9lketj0","ConstructionMaterials",charset='utf8')
    cursor = db.cursor()
    with open('/root/Spider_Project/data/focus_city_url.csv','r') as city_url_file:
        for url_info in city_url_file.readlines()[3000:5000]:
            time.sleep(0.3)
            city_f_province_id = url_info.split('\t')[1].strip()
            city_f_city_id = url_info.split('\t')[2].strip()
            city_basic_url = url_info.split('\t')[3].strip()
            salse_status = {
            '待售':1,
            '在售':2,
            '售完':3,
            '出租':2,
            '租售':2,
            }
            try:
                headers = [
                    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0; Baiduspider-ads) Gecko/17.0 Firefox/17.0",
                    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4",
                    "Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; BIDUBrowser 7.6)",
                    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
                    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
                    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
                    ]
                # 法1
                # opener = urllib.request.build_opener()
                # opener.add_headers = [{'User-Agent':choice(headers)}]
                # data_requests = opener.open(city_basic_url,timeout=20).read().decode('utf8')
                time.sleep(1)
                opr = makeMyOpener()
                uop = opr.open(city_basic_url, timeout = 1000)
                data_requests = uop.read().decode('utf8')
                # 法2
                # proxies = {
                #          "http":"http://"+choice(get_ip()),
                #          "https":"https://"+choice(get_ip())
                #     }
                # proxy_support = urllib.request.ProxyHandler(proxies)
                # opener = urllib.request.build_opener(proxy_support)
                # opener.add_headers = [{'User-Agent':choice(headers)}]
                # urllib.request.install_opener(opener)
                # data_requests = urllib.request.urlopen(city_basic_url,timeout=20).read().decode("utf8")

                # 法3
                # print(data_requests)
                # data_requests = requests.get(city_basic_url,headers={'User-Agent':choice(headers)},proxies=proxies)
                # data_requests.encoding = 'utf-8'

                soup = BeautifulSoup(data_requests,'html.parser')
                c_f_link = city_basic_url.replace('/xiangxi／','.html')
                c_f_name = soup.select('h1')[1]['title']
                c_f_province_id = int(city_f_province_id)
                c_f_city_id = int(city_f_city_id)
                c_f_area_id = 0
                # 毛胚总户数
                c_f_rough_door_count = 0
                # 精装总户数
                c_f_good_door_count = 0
                # 当期毛胚户数
                c_f_now_rough_door_count = 0
                # 当期精装总户数
                c_f_now_good_door_count = 0
                # 精装标准 元/平米
                c_f_redecorate_price = ''
                # 物业类型
                c_f_property = ''
                # 工程进度
                c_f_progress = ''
                # 均价
                try:
                    c_f_price = soup.select('table.price-tb tbody tr td.tleft')[0].text.strip()
                except:
                    c_f_price = ''
                # 是否有样板房 0=否 1=是
                c_f_have_demo = 0
                # 样板房配套品牌
                c_f_demo_brand = ''
                # 详细地址
                c_f_address = ''
                # 环线位置
                c_f_metro_info = ''
                # 销售状态
                c_f_salse_status = 2
                # 开发商
                c_f_developer = ''
                # 装修状态
                c_f_redecorate_type = ''
                # 总户数
                c_f_door_count = 0
                # 户型及户数
                c_f_brunt = ''
                # 楼栋总数
                c_f_building_count = 0
                # 楼层状况
                c_f_floor_status = ''
                # 占地面积
                c_f_area_covered = ''
                # 建筑面积
                c_f_built_up  = ''
                # 产权
                c_f_property_right = ''
                # 物业公司
                c_f_property_firm = ''
                # 开盘时间
                try:
                    c_f_open_time = soup.select('table.open-info-tb > tbody > tr > td')[0].text.strip('\r\n  ')
                except:
                    c_f_open_time = ''
                # 交房时间
                try:
                    c_f_others_time = soup.select('table.live-info-tb tbody tr td')[0].text.strip()
                except:
                    c_f_others_time = ''
                # print(f_others_time)
                # 售楼电话
                c_f_salse_telphone = ''
                # 售楼地址
                c_f_salse_address = ''

                all_info_list = soup.select('div.loupan-detail-mod ul li')
                for all_info in all_info_list:
                    # print(all_info.text)
                    if '建筑形式' in all_info.text:
                        # print(all_info.text)
                        c_f_floor_status = str(all_info.text.split('：')[1].strip())
                    if '楼盘位置' in all_info.text:
                        # print(all_info.text)
                        c_f_address = str(all_info.text.split('：')[1].strip())
                    if '环线位置' in all_info.text:
                        # print(all_info.text)
                        c_f_metro_info = str(all_info.text.split('：')[1].strip())
                    if '咨询电话' in all_info.text:
                        # print(all_info.text)
                        c_f_salse_telphone = str(all_info.text.split('：')[1].strip())
                    if '售楼地址' in all_info.text:
                        c_f_salse_address = str(all_info.text.split('售楼地址：')[1].strip())
                    if '开 发  商' in all_info.text:
                        c_f_developer = str(all_info.text.split('：')[1].strip())
                    if '户    型' in all_info.text:
                        c_f_brunt = str(all_info.text.split('：')[1].replace('\r','').replace(' ','').replace('\n',''))
                    if '建筑面积' in all_info.text:
                        c_f_built_up = str(all_info.text.split('：')[1].strip())
                    if '产权年限' in all_info.text:
                        c_f_property_right = str(all_info.text.split('：')[1].strip())
                    if '占地面积' in all_info.text:
                        c_f_area_covered = str(all_info.text.split('：')[1].strip())
                    if '物业公司' in all_info.text:
                        c_f_property_firm = str(all_info.text.split('：')[1].strip())
                    if '装修情况' in all_info.text:
                        c_f_redecorate_type = str(all_info.text.split('：')[1].strip())
                    if '总 户  数' in all_info.text:
                        c_f_door_count = int(all_info.text.split('：')[1].strip())
                    if '楼栋总数' in all_info.text:
                        c_f_building_count = int(all_info.text.split('：')[1].strip())
                with open('/root/Spider_Project/data/cm_area.csv','r') as cm_area_csv_file:
                    for cm_area_items in cm_area_csv_file.readlines():
                        cm_area_item = cm_area_items.split(',')
                        if cm_area_item[2].split('"')[1] in c_f_address:
                            c_f_area_id = int(cm_area_item[0].split('"')[1])
                            # print(c_f_area_id)
                c_f_record_time = int(time.time())
                c_f_update_time = int(time.time())
                # print(c_f_record_time,c_f_update_time,c_f_link,c_f_name,c_f_province_id,c_f_city_id,c_f_area_id,c_f_address,c_f_metro_info,c_f_salse_status,c_f_developer,c_f_redecorate_type,c_f_door_count,c_f_rough_door_count,c_f_good_door_count,c_f_now_rough_door_count,c_f_now_good_door_count,c_f_brunt,c_f_redecorate_price,c_f_building_count,c_f_floor_status,c_f_progress,c_f_area_covered,c_f_built_up,c_f_property_right,c_f_property,c_f_property_firm,c_f_price,c_f_have_demo,c_f_demo_brand,c_f_open_time,c_f_others_time,c_f_salse_telphone,c_f_salse_address)

                # threadLock.acquire()
                try:
                    search_sql = "SELECT * FROM cm_data_focus WHERE f_name = '{}';".format(c_f_name)
                    # print(search_sql)
                    cursor.execute(search_sql)
                    # print(cursor.fetchall())
                    if len(cursor.fetchall()):
                        update_sql = "UPDATE cm_data_focus SET f_update_time={},f_link='{}', f_name='{}', f_province_id={}, f_city_id={}, f_area_id={}, f_address='{}', f_metro_info='{}', f_salse_status={}, f_developer='{}', f_redecorate_type='{}', f_door_count={}, f_rough_door_count={}, f_good_door_count={}, f_now_rough_door_count={}, f_now_good_door_count={}, f_brunt='{}', f_redecorate_price='{}', f_building_count={}, f_floor_status='{}', f_progress='{}', f_area_covered='{}', f_built_up='{}', f_property_right='{}', f_property='{}', f_property_firm='{}', f_price='{}', f_have_demo={}, f_demo_brand='{}', f_open_time='{}', f_others_time='{}', f_salse_telphone='{}',f_salse_address='{}'".format(c_f_update_time,c_f_link,c_f_name,c_f_province_id,c_f_city_id,c_f_area_id,c_f_address,c_f_metro_info,c_f_salse_status,c_f_developer,c_f_redecorate_type,c_f_door_count,c_f_rough_door_count,c_f_good_door_count,c_f_now_rough_door_count,c_f_now_good_door_count,c_f_brunt,c_f_redecorate_price,c_f_building_count,c_f_floor_status,c_f_progress,c_f_area_covered,c_f_built_up,c_f_property_right,c_f_property,c_f_property_firm,c_f_price,c_f_have_demo,c_f_demo_brand,c_f_open_time,c_f_others_time,c_f_salse_telphone,c_f_salse_address)+"WHERE f_name = '{}';".format(c_f_name)
                        cursor.execute(update_sql)
                        db.commit()
                        print(c_f_name,'Focus update success')
                    else:
                        insert_sql = "INSERT INTO cm_data_focus (f_record_time,f_update_time,f_link, f_name, f_province_id, f_city_id, f_area_id, f_address, f_metro_info, f_salse_status, f_developer, f_redecorate_type, f_door_count, f_rough_door_count, f_good_door_count, f_now_rough_door_count, f_now_good_door_count, f_brunt, f_redecorate_price, f_building_count, f_floor_status, f_progress, f_area_covered, f_built_up, f_property_right, f_property, f_property_firm, f_price, f_have_demo, f_demo_brand, f_open_time, f_others_time, f_salse_telphone,f_salse_address) VALUES ({},{},'{}','{}',{},{},{},'{}','{}',{},'{}','{}',{},{},{},{},{},'{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}');".format(c_f_record_time,c_f_update_time,c_f_link,c_f_name,c_f_province_id,c_f_city_id,c_f_area_id,c_f_address,c_f_metro_info,c_f_salse_status,c_f_developer,c_f_redecorate_type,c_f_door_count,c_f_rough_door_count,c_f_good_door_count,c_f_now_rough_door_count,c_f_now_good_door_count,c_f_brunt,c_f_redecorate_price,c_f_building_count,c_f_floor_status,c_f_progress,c_f_area_covered,c_f_built_up,c_f_property_right,c_f_property,c_f_property_firm,c_f_price,c_f_have_demo,c_f_demo_brand,c_f_open_time,c_f_others_time,c_f_salse_telphone,c_f_salse_address)
                        cursor.execute(insert_sql)
                        db.commit()
                        print(c_f_name,'Focus success commit')
                except Exception as e:
                    print(e)
                    db.rollback()

                # threadLock.release()
            except Exception as e:
                # print(data_requests)
                # print(all_info_list)
                print(e,'---',city_basic_url)
    db.close()

if __name__ == '__main__':
    # # 1.获取城市的网站链接
    # get_focus_city_code()
    # time.sleep(5)

    # # 2.保存所有城市的具体楼盘信息
    # with open('/root/Spider_Project/data/focus_city_list.csv','r') as city_code_info_file:
    #     for city_list_info in city_code_info_file.readlines():
    #         time.sleep(0.3)
    #         get_url_save(city_list_info)
    # time.sleep(5)

    # 3.获取具体信息并插入
    # proxies_list = []
    # with open('/root/Spider_Project/data/proxies_file.csv','r') as proxies_file:
    #     for proxies in proxies_file:
    #         proxies_list.append(proxies.strip())
    get_focus_info()
    print (time.ctime(time.time()),"Focus Finish")
