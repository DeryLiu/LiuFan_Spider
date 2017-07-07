import requests
from bs4 import BeautifulSoup
import re
import random
import sys
import time
import threading
from random import choice
import requests
from bs4 import BeautifulSoup
import simplejson
import urllib.request
import pymysql

# http://m.db.house.qq.com/search//{}/?ajax=1&city={}&pno=0

def get_proxies_ip():
    # MAX_RETRIES = 20
    # session = requests.Session()
    # adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
    # session.mount('https://', adapter)
    # session.mount('http://', adapter)
    # rp = session.get(url)
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

# part1
def get_all_cityNkey():
     # -----获取所有城市及其对应key------
    url = 'http://db.house.qq.com/index.php?mod=search&city=bj#LXNob3d0eXBlXzE='
    city_request = requests.get(url)
    soup = BeautifulSoup(city_request.text,'html.parser')
    city_list_t = soup.select('div.scrollContent dl dd a')

    # 获得城市的list
    city_list = []
    with open('/root/Spider_Project/data/cm_city.csv','r') as city_file:
        for city_info in city_file.readlines():
            city_list.append([city.strip('",\n') for city in city_info.split(',')])
        # print(city_list)

    with open('/root/Spider_Project/data/tencent_city_list.csv','w') as city_file:
        for c in city_list_t:
            for city_name in city_list:
                if c.text in city_name[2]:
                    city_file.write(c.text+'\t'+city_name[1]+'\t'+city_name[0]+'\t'+c['href'].split('=')[-1]+'\n')

# 爬取新的代理ip
def get_ip():
    """获取代理IP"""
    url = "http://www.xicidaili.com/nn"
    headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
                "Accept-Encoding":"gzip, deflate, sdch",
                "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
                "Referer":"http://www.xicidaili.com",
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
                }
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = soup.table.find_all("td")
    ip_compile= re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')    # 匹配IP
    port_compile = re.compile(r'<td>(\d+)</td>')                # 匹配端口
    ip = re.findall(ip_compile,str(data))       # 获取所有IP
    port = re.findall(port_compile,str(data))   # 获取所有端口
    # print([":".join(i) for i in zip(ip,port)])
    return [":".join(i) for i in zip(ip,port)]  # 组合IP+端口，如：115.112.88.23:8080


def get_info(province_code,city_num,city_code):
        try:
            salse_status = {
            '待售':1,
            '在售':2,
            '售完':3,
            '出租':2,
            '租售':2,
            }
            city_url = 'http://m.db.house.qq.com/search//{c_code}/?ajax=1&city={c_code}&pno=0'.format(c_code=city_code)
            # print(city_url)
            headers ={
                'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
            }
            opener = urllib.request.build_opener()
            # urllib.request.install_opener(opener)
            # html = urllib.request.urlopen("http://www.111cn.net ",headers).read().decode("utf8")
            opener.add_headers = [headers]
            html = opener.open(city_url,timeout=20).read().decode('utf-8')
            # soup = BeautifulSoup(html, 'html.parser')
            # data_request = requests.get(city_url,headers=headers,proxies=proxies,timeout=20)
            # data_request.encoding = 'utf-8'
            # soup = BeautifulSoup(data_request.text,'html.parser')
            info_dict = simplejson.loads(html)
            info_data_list = info_dict['data']['list']

            for info in info_data_list:
                c_f_record_time = int(time.time())
                c_f_update_time = int(time.time())
                c_f_link = info['FUrl']
                c_f_name = info['FName']
                c_f_province_id = province_code
                c_f_city_id = city_num
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
                c_f_price = info['FPrice']
                # 是否有样板房 0=否 1=是
                c_f_have_demo = 0
                # 样板房配套品牌
                c_f_demo_brand = ''
                # 详细地址
                c_f_address = info['FAddress']
                # 环线位置
                c_f_metro_info = ''
                # 销售状态
                try:
                    c_f_salse_status = salse_status[info['FSellStatusStr']]
                except:
                    c_f_salse_status = 2
                # 开发商
                c_f_developer = info['FDeveloper']
                # 装修状态
                try:
                    c_f_redecorate_type = info['FDecorationArr'][0]
                except:
                    c_f_redecorate_type = ''
                # 总户数
                c_f_door_count = 0
                # 户型及户数
                try:
                    c_f_brunt = info['FUnitArr'][0][['FName']]
                except:
                    c_f_brunt = ''
                # 楼栋总数
                c_f_building_count = 0
                # 楼层状况
                try:
                    c_f_floor_status = info['FBuildTypeArr'][0]['FName']
                except:
                    c_f_floor_status = ''
                # 占地面积
                c_f_area_covered = ''
                # 建筑面积
                c_f_built_up  = ''
                # 产权
                c_f_property_right = info['FYears']
                # 物业公司
                c_f_property_firm = ''
                # 开盘时间
                c_f_open_time = info['FOpenDate']
                # 交房时间
                c_f_others_time = info['FInDate']
                # 售楼电话
                c_f_salse_telphone = info['FPhoneArr']['phone']
                # 售楼地址
                c_f_salse_address = ''

                with open('/root/Spider_Project/data/cm_area.csv','r') as cm_area_csv_file:
                    for cm_area_items in cm_area_csv_file.readlines():
                        cm_area_item = cm_area_items.split(',')
                        if cm_area_item[2].split('"')[1] in c_f_address:
                            c_f_area_id = cm_area_item[0].split('"')[1]
                            # print(c_f_area_id)
                # print(c_f_record_time,c_f_update_time,c_f_link,c_f_name,c_f_province_id,c_f_city_id,c_f_area_id,c_f_address,c_f_metro_info,c_f_salse_status,c_f_developer,c_f_redecorate_type,c_f_door_count,c_f_rough_door_count,c_f_good_door_count,c_f_now_rough_door_count,c_f_now_good_door_count,c_f_brunt,c_f_redecorate_price,c_f_building_count,c_f_floor_status,c_f_progress,c_f_area_covered,c_f_built_up,c_f_property_right,c_f_property,c_f_property_firm,c_f_price,c_f_have_demo,c_f_demo_brand,c_f_open_time,c_f_others_time,c_f_salse_telphone,c_f_salse_address)

                try:
                    search_sql = "SELECT * FROM cm_data_tencent WHERE f_name = '{}';".format(c_f_name)
                    # print(search_sql)
                    cursor.execute(search_sql)
                    if len(cursor.fetchall()):
                        update_sql = "UPDATE cm_data_tencent SET f_update_time={},f_link='{}', f_name='{}', f_province_id={}, f_city_id={}, f_area_id={}, f_address='{}', f_metro_info='{}', f_salse_status={}, f_developer='{}', f_redecorate_type='{}', f_door_count={}, f_rough_door_count={}, f_good_door_count={}, f_now_rough_door_count={}, f_now_good_door_count={}, f_brunt='{}', f_redecorate_price='{}', f_building_count={}, f_floor_status='{}', f_progress='{}', f_area_covered='{}', f_built_up='{}', f_property_right='{}', f_property='{}', f_property_firm='{}', f_price='{}', f_have_demo={}, f_demo_brand='{}', f_open_time='{}', f_others_time='{}', f_salse_telphone='{}',f_salse_address='{}'".format(c_f_update_time,c_f_link,c_f_name,c_f_province_id,c_f_city_id,c_f_area_id,c_f_address,c_f_metro_info,c_f_salse_status,c_f_developer,c_f_redecorate_type,c_f_door_count,c_f_rough_door_count,c_f_good_door_count,c_f_now_rough_door_count,c_f_now_good_door_count,c_f_brunt,c_f_redecorate_price,c_f_building_count,c_f_floor_status,c_f_progress,c_f_area_covered,c_f_built_up,c_f_property_right,c_f_property,c_f_property_firm,c_f_price,c_f_have_demo,c_f_demo_brand,c_f_open_time,c_f_others_time,c_f_salse_telphone,c_f_salse_address)+"WHERE f_name = '{}';".format(c_f_name)
                        cursor.execute(update_sql)
                        db.commit()
                        print(c_f_name,'Tencent update success')
                    else:
                        insert_sql = "INSERT INTO cm_data_tencent (f_record_time,f_update_time,f_link, f_name, f_province_id, f_city_id, f_area_id, f_address, f_metro_info, f_salse_status, f_developer, f_redecorate_type, f_door_count, f_rough_door_count, f_good_door_count, f_now_rough_door_count, f_now_good_door_count, f_brunt, f_redecorate_price, f_building_count, f_floor_status, f_progress, f_area_covered, f_built_up, f_property_right, f_property, f_property_firm, f_price, f_have_demo, f_demo_brand, f_open_time, f_others_time, f_salse_telphone,f_salse_address) VALUES ({},{},'{}','{}',{},{},{},'{}','{}',{},'{}','{}',{},{},{},{},{},'{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}');".format(c_f_record_time,c_f_update_time,c_f_link,c_f_name,c_f_province_id,c_f_city_id,c_f_area_id,c_f_address,c_f_metro_info,c_f_salse_status,c_f_developer,c_f_redecorate_type,c_f_door_count,c_f_rough_door_count,c_f_good_door_count,c_f_now_rough_door_count,c_f_now_good_door_count,c_f_brunt,c_f_redecorate_price,c_f_building_count,c_f_floor_status,c_f_progress,c_f_area_covered,c_f_built_up,c_f_property_right,c_f_property,c_f_property_firm,c_f_price,c_f_have_demo,c_f_demo_brand,c_f_open_time,c_f_others_time,c_f_salse_telphone,c_f_salse_address)
                        cursor.execute(insert_sql)
                        db.commit()
                        print(c_f_name,'Tencent commit success')
                except Exception as e:
                    print(e)
                    db.rollback()
                # sql = "INSERT INTO cm_data_tencent (f_record_time,f_update_time,f_link, f_name, f_province_id, f_city_id, f_area_id, f_address, f_metro_info, f_salse_status, f_developer, f_redecorate_type, f_door_count, f_rough_door_count, f_good_door_count, f_now_rough_door_count, f_now_good_door_count, f_brunt, f_redecorate_price, f_building_count, f_floor_status, f_progress, f_area_covered, f_built_up, f_property_right, f_property, f_property_firm, f_price, f_have_demo, f_demo_brand, f_open_time, f_others_time, f_salse_telphone,f_salse_address) VALUES ({},{},'{}','{}',{},{},{},'{}','{}',{},'{}','{}',{},{},{},{},{},'{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}')".format(c_f_record_time,c_f_update_time,c_f_link,c_f_name,c_f_province_id,c_f_city_id,c_f_area_id,c_f_address,c_f_metro_info,c_f_salse_status,c_f_developer,c_f_redecorate_type,c_f_door_count,c_f_rough_door_count,c_f_good_door_count,c_f_now_rough_door_count,c_f_now_good_door_count,c_f_brunt,c_f_redecorate_price,c_f_building_count,c_f_floor_status,c_f_progress,c_f_area_covered,c_f_built_up,c_f_property_right,c_f_property,c_f_property_firm,c_f_price,c_f_have_demo,c_f_demo_brand,c_f_open_time,c_f_others_time,c_f_salse_telphone,c_f_salse_address)+" ON DUPLICATE KEY UPDATE f_record_time={},f_update_time={},f_link='{}', f_name='{}', f_province_id={}, f_city_id={}, f_area_id={}, f_address='{}', f_metro_info='{}', f_salse_status={}, f_developer='{}', f_redecorate_type='{}', f_door_count={}, f_rough_door_count={}, f_good_door_count={}, f_now_rough_door_count={}, f_now_good_door_count={}, f_brunt='{}', f_redecorate_price='{}', f_building_count={}, f_floor_status='{}', f_progress='{}', f_area_covered='{}', f_built_up='{}', f_property_right='{}', f_property='{}', f_property_firm='{}', f_price='{}', f_have_demo={}, f_demo_brand='{}', f_open_time='{}', f_others_time='{}', f_salse_telphone='{}',f_salse_address='{}';" .format(c_f_record_time,c_f_update_time,c_f_link,c_f_name,c_f_province_id,c_f_city_id,c_f_area_id,c_f_address,c_f_metro_info,c_f_salse_status,c_f_developer,c_f_redecorate_type,c_f_door_count,c_f_rough_door_count,c_f_good_door_count,c_f_now_rough_door_count,c_f_now_good_door_count,c_f_brunt,c_f_redecorate_price,c_f_building_count,c_f_floor_status,c_f_progress,c_f_area_covered,c_f_built_up,c_f_property_right,c_f_property,c_f_property_firm,c_f_price,c_f_have_demo,c_f_demo_brand,c_f_open_time,c_f_others_time,c_f_salse_telphone,c_f_salse_address)
                # try:
                #     # 执行SQL语句
                #     cursor.execute(sql)
                #     db.commit()
                #
                #     print('success commit')
                # except Exception as e:
                #     print(e)
                #     # 发生错误时回滚
                #     db.rollback()

        except Exception as e:
            print(city_url,'-------',e)
            get_info(province_code,city_num,city_code)

if __name__ == '__main__':
    # # 1.先把所有的city和id写入文件tencent_city_list.csv
    # get_all_cityNkey()
    # time.sleep(5)

    # 2.
    with open('/root/Spider_Project/data/tencent_city_list.csv','r') as city_code_file:
        db = pymysql.connect("192.168.1.231","root","3jw9lketj0","ConstructionMaterials",charset='utf8')
        cursor = db.cursor()
        for city_list_info in city_code_file.readlines():
            new_city_list = city_list_info.split('\t')
            province_id = new_city_list[1]
            city_code_id = new_city_list[2]
            city_id = new_city_list[3].strip()
            t_city_info = threading.Thread(target=get_info,args=(province_id,city_code_id,city_id))
            t_city_info.start()
            time.sleep(0.3)
            get_info(province_id,city_code_id,city_id)
        db.close()


