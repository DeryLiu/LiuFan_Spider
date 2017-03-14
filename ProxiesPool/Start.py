from HtmlParser import Html_Parser
import config
import requests
import pymysql
import time
from multiprocessing import Pool,Lock

headers = config.get_header()

proxie_type = {
    '高匿代理':0,
    '透明':1
}

def get_proxy_ip():
    global lock
    lock = Lock()
    xmlpar = Html_Parser()
    for parxml in config.parserList:
        for url in parxml['urls']:
            try:
                req = requests.get(url,headers=headers)
                req.encoding = parxml['encode']
            except:
                print('error')
            if parxml['type'] == 'xpath':
                xrpath = xmlpar.XpathPraser(req.text,parxml)
            else:
                xrpath = xmlpar.RegularPraser(req.text,parxml)
            # print(xrpath)
            pool = Pool(10)
            pool.map(save_to_db,xrpath)
            pool.close()
            pool.join()

def save_to_db(info_dict):
    print(info_dict)
    db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    # db = pymysql.connect("192.168.1.231","root","3jw9lketj0","ConstructionMaterials",charset='utf8')
    cursor = db.cursor()
    update_time = int(time.time())
    url = 'http://www.baidu.com'

    proxies = {
        'http':'http://'+info_dict['ip']+':'+str(info_dict['port'])
    }
    MAX_RETRIES = 20
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    rp = session.get(url)
    try:
        rp = requests.get(url,headers=headers,proxies=proxies,timeout=10)
        if rp.status_code == 200:
            lock.acquire()
            insert_sql = "INSERT INTO proxies_info(p_ip,p_port,p_type, p_protocol, p_country,p_updatetime,p_area,p_speed) VALUES ('{}',{},{},{},'{}',{},'{}','{}');".format(info_dict['ip'],info_dict['port'],info_dict['types'],info_dict['protocol'],info_dict['country'],update_time,info_dict['area'],info_dict['speed'])
            try:
                cursor.execute(insert_sql)
                db.commit()
                print(info_dict['ip'])
            except:
                print('db error')
                db.rollback()
            lock.release()
    except:
        print(info_dict['ip'] ,'requests error')
    db.close()

# ------------------------------

def delet_ip(proxies_pp):
    db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    # db = pymysql.connect("192.168.1.231","root","3jw9lketj0","ConstructionMaterials",charset='utf8')
    cursor = db.cursor()
    try:
        url = 'http://www.baidu.com'
        proxies = {
            'http':'http://'+proxies_pp
        }
        # MAX_RETRIES = 20
        # url ='http://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi'
        #
        # session = requests.Session()
        # adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
        # session.mount('https://', adapter)
        # session.mount('http://', adapter)
        # r = session.get(url)
        # print(r.content)

        rp = requests.get(url,headers=headers,proxies=proxies,timeout=10)
        if rp.status_code != 200:
            lock.acquire()
            delect_sql = "DELETE FROM proxies_info WHERE p_ip ='{}'".format(proxies_pp.split(':')[0])
            try:
                cursor.execute(delect_sql)
                db.commit()
                print(proxies_pp)
            except:
                db.rollback()
            lock.release()
    except Exception as e:
        lock.acquire()
        delect_sql = "DELETE FROM proxies_info WHERE p_ip ='{}';".format(proxies_pp.split(':')[0])
        try:
            cursor.execute(delect_sql)
            db.commit()
            print(proxies_pp)
        except:
            db.rollback()
        lock.release()
    db.close()

def clean_handle():
    global lock
    lock = Lock()
    db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    # db = pymysql.connect("192.168.1.231","root","3jw9lketj0","ConstructionMaterials",charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM proxies_info;"
    proxies_list = []
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            proxy_ip = row[1]
            proxy_port = str(row[2])
            proxies_list.append(proxy_ip+':'+proxy_port)
    except:
        db.rollback()
        print('db error')
    db.close()

    pool = Pool(30)
    pool.map(delet_ip,proxies_list)
    pool.close()
    pool.join()

if __name__ == "__main__":
    get_proxy_ip()
    time.sleep(2)
    clean_handle()
