# import requests
# url = 'http://www.taobao.com'
# MAX_RETRIES = 20
# session = requests.Session()
# adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
# session.mount('https://', adapter)
# session.mount('http://', adapter)
# rp = session.get(url)
# rp.encoding = 'gb2312'
# print(rp.content)

import pymysql
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

print(get_proxies_ip())