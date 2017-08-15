from bs4 import BeautifulSoup
import requests, re
import random, pymysql
import time, json
from multiprocessing import Pool, Lock
from selenium import webdriver

'王  账号：18917858587    密码：858587     ssh -D 9050 -p924 pi@120.55.168.199     fangquan()**'
'郑  账号：JTL20170427    密码：123456     ssh -D 9050 -p923 pi@120.55.168.199     fangquan()$$'


def get_proxies_ip():
    # MAX_RETRIES = 20
    # session = requests.Session()
    # adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
    # session.mount('https://', adapter)
    # session.mount('http://', adapter)
    # rp = session.get(url)
    db = pymysql.connect("localhost", "root", "123456", "Spider_Data", charset='utf8')
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
            proxies_list.append(proxy_ip + ':' + proxy_port)
    except:
        db.rollback()
    db.close()
    proxies = {
        'http': 'http://' + random.choice(proxies_list)
    }
    return random.choice(proxies_list)


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
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
    }
    return headers


def save_url_info():
    '''
    0  参考项目
    1  精选项目
    2  全部项目
    '''
    error_file = open('error.csv', 'w')
    # 拟在建-精选 422
    # url_list = ['http://center.qianlima.com/xiangmu_centerdata.jsp?pg={}&dengji=0&stype=0&uid=0&sheng=&shi=&jzjd=&xmlb=&xmmc=&gxmc=&protype=1&findAgain=false&callback=jsonpCallback1'.format(i) for i in range(1,422)]

    # 拟在建-普通 465
    url_list = [
        'http://center.qianlima.com/xiangmu_centerdata.jsp?dengji=0&stype=0&uid=0&sheng=-1&shi=&jzjd=&xmlb=-1&xmzlb=-1&xmmc=&gxmc=&protype=0&findAgain=false&pg={}&callback=jsonpCallback0'.format(
            i) for i in range(1, 465)]

    # with open('NiZaiJian_Good_Url_NEW.csv','w') as NiZaiJian_Good_Url_File:
    with open('NiZaiJian_Normal_Url_NEW.csv', 'w') as NiZaiJian_Good_Url_File:
        for url in url_list:
            try:
                # time.sleep(1) ,proxies={'http':'http://'+get_proxies_ip()}
                reponse = requests.get(url, headers=get_headers(), timeout=80)
                return_json = reponse.text
                project_id_list = re.findall('"cid\":(.*?),', return_json, re.S)
                project_name_list = re.findall('"title\":\"(.*?)\"', return_json, re.S)
                project_url_list = re.findall('"url\":\"(.*?)\"', return_json, re.S)
                project_area_list = re.findall('"diqu\":\"(.*?)\"', return_json, re.S)
                project_yz_list = re.findall('"yz\":\"(.*?)\"', return_json, re.S)
                project_jzjd_list = re.findall('"jzjd\":\"(.*?)\"', return_json, re.S)
                project_xmlb_list = re.findall('"xmlb\":\"(.*?)\"', return_json, re.S)
                project_zx_list = re.findall('"zx\":\"(.*?)\"', return_json, re.S)
                project_tzje_list = re.findall('"tzje\":\"(.*?)\"', return_json, re.S)
                project_updatetime_list = re.findall('"updatetime\":\"(.*?)\"', return_json, re.S)
                for i in range(len(project_id_list)):
                    NiZaiJian_Good_Url_File.write(
                        project_id_list[i] + ',' + project_name_list[i] + ',' + project_url_list[i] + ',' +
                        project_area_list[i] + ',' + project_yz_list[i] + ',' + project_jzjd_list[i] + ',' +
                        project_xmlb_list[i] + ',' + project_zx_list[i] + ',' + project_tzje_list[i] + ',' +
                        project_updatetime_list[i] + '\n')
                    print(project_name_list[i])
            except Exception as e:
                error_file.write(url + '\n')
                print('findError', url, e)


def save_vip_url_handle():
    global error_file, NiZaiJian_VIP_Url_File, lock
    error_file = open('error.csv', 'w')
    NiZaiJian_VIP_Url_File = open('NiZaiJian_VIP_Url_NEW.csv', 'w')
    lock = Lock()

    all_url_list = ['http://www.qianlima.com/common/yezhu_vip_list.jsp?xx=0&pageNo={}'.format(i) for i in range(499)]
    url_list = []
    for url in all_url_list:
        url_list.append(url)
    pool = Pool(20)
    pool.map(save_vip_url, url_list)
    pool.close()
    pool.join()

    error_file.close()
    NiZaiJian_VIP_Url_File.close()


def save_vip_url(url):
    try:
        # time.sleep(1)
        reponse = requests.get(url, headers=get_headers(), timeout=60)
        reponse.encoding = 'gbk'
        return_json = reponse.text
        soup = BeautifulSoup(return_json, 'html.parser')
        # 项目名称
        project_title = soup.select('div.item_name > dl > dt > a')
        project_area_list = soup.select('div.city_name')
        for project_i in range(len(project_title)):
            project_url = project_title[project_i]['href']
            project_name = project_title[project_i].text.strip().replace(',', '_')
            project_area = project_area_list[project_i + 1].text.strip()
            # print(project_url,project_name,project_area)
            lock.acquire()
            NiZaiJian_VIP_Url_File.write(project_url + ',' + project_name + ',' + project_area + '\n')
            NiZaiJian_VIP_Url_File.flush()
            lock.release()
            print(project_name)
    except Exception as e:
        lock.acquire()
        # aaa.append(url.split('=')[2])
        error_file.write(url.split('=')[2] + ',')
        error_file.flush()
        lock.release()
        print('findError', url, e)


def save_data_inDB():
    db = pymysql.connect("localhost","root","xxx","xxx",charset='utf8')
    # cursor = db.cursor()

    sleep_time = [5, 6, 7, 8, 9, 10, 12, 11, 13, 14, 15]

    # chrome
    # chrome driver 设置代理
    PROXY_IP = get_proxies_ip() #
    print(PROXY_IP)
    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server={}".format('183.131.215.86:8080'))
    driver = webdriver.Chrome(executable_path="/Users/Dery/SeleniumWebDriver/chromedriver",chrome_options=options)

    # driver = webdriver.Chrome(executable_path="/Users/Dery/SeleniumWebDriver/chromedriver")

    driver.get("http://center.qianlima.com/login.jsp")
    driver.find_element_by_id('abc').clear()
    driver.find_element_by_id('abc').send_keys('xxx')
    # driver.find_element_by_id('abc').send_keys('xxx')
    driver.find_element_by_css_selector('#kuang > fieldset > input:nth-of-type(2)').clear()
    driver.find_element_by_css_selector('#kuang > fieldset > input:nth-of-type(2)').send_keys('xxx')
    # driver.find_element_by_css_selector('#kuang > fieldset > input:nth-of-type(2)').send_keys('xxx')
    driver.find_element_by_css_selector("#deng").click()
    print('login')

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'Cache-Control': 'max-age=0',
               'Cookie': 'UM_distinctid=15ce761eab920d-0b4eadc523c05-30667808-1fa400-15ce761eabb0; gr_user_id=292fdbf5-f453-4933-8858-3e4a285a4d08; qlm_username=JTL20170427; qlm_password=gmuBRU3fjfEB7fBEEg7ogu7KCpuC883g; rem_login=1; __jsluid=f849c55868bc30b41cfa5973310bbc9f; qlmll_his=",29773672,"; Hm_lvt_0a38bdb0467f2ce847386f381ff6c0e8=1498530573; Hm_lpvt_0a38bdb0467f2ce847386f381ff6c0e8=1498530692; Hm_lvt_5dc1b78c0ab996bd6536c3a37f9ceda7=1498530573; Hm_lpvt_5dc1b78c0ab996bd6536c3a37f9ceda7=1498530705; CNZZDATA1848524=cnzz_eid%3D1262932576-1498527022-%26ntime%3D1498529096; gr_session_id_83e3b26ab9124002bae03256fc549065=aab205b4-5ce8-4b9f-a068-336929156460',
               'Host': 'www.qianlima.com',
               'Referer': 'http://www.qianlima.com/jxxm/',
               'Proxy-Connection': 'keep-alive',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
               }

            # with open('NiZaiJian_Good_Url_0525.csv', 'r') as NiZaiJian_Url_file:
            #     for NiZaiJian_url in NiZaiJian_Url_file.readlines()[8930:9029]:

            # with open('NiZaiJian_Normal_Url_0525.csv','r') as NiZaiJian_Url_file:
            #     for NiZaiJian_url in NiZaiJian_Url_file.readlines()[2044:2155]:

            # project_ID = NiZaiJian_url.split(',')[0]
            # project_name = NiZaiJian_url.split(',')[1]
            # project_url = NiZaiJian_url.split(',')[2]
            # project_area = NiZaiJian_url.split(',')[3]
            # update_Time = NiZaiJian_url.split(',')[-1]

    with open('NiZaiJian_VIP_Url_0526.csv','r') as NiZaiJian_Url_file:
        for NiZaiJian_url in NiZaiJian_Url_file.readlines()[2195:2294]:
            project_url,project_name,project_area = NiZaiJian_url.split(',')

            lfTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            time.sleep(random.choice(sleep_time))
            try:
                # 1.
                driver.get(project_url)
                soup = BeautifulSoup(driver.page_source,'html.parser')
                # 2.,proxies={'http':'http://182.92.81.200:8080'}
                # response = requests.get(project_url, headers=headers, timeout=30)
                # soup = BeautifulSoup(response.text, 'html.parser')
                # # info
                try:
                    update_Time = soup.select('dl > dt > span.clock')[0].text.split('：')[1]
                except:
                    update_Time = ' '

                fbsj = soup.select('dl.daoxiao1 > dt > span.clock1')[0].text
                # print(fbsj)
                # 项目跟进：
                xmgj_info_list = soup.select('div.zhengC > table')[0].text.split('\n')
                QLM_xmgj = []
                xmgj_count = int((len(xmgj_info_list) - 2) / 6 - 1)
                for xmgj_i in range(1, xmgj_count + 1):
                    QLM_xmgj.append({'日期': xmgj_info_list[2 + 6 * xmgj_i], '版本': xmgj_info_list[3 + 6 * xmgj_i],
                                     '进展阶段': xmgj_info_list[4 + 6 * xmgj_i], '进展备注': xmgj_info_list[5 + 6 * xmgj_i]})
                # print(QLM_xmgj)
                # 项目概况：
                xmgk_info_list = soup.select('div.zhengC > table')[1].text
                # print(xmgk_info_list)
                xmbh = re.findall('项目编号(.*?)跟进记录', xmgk_info_list, re.S)[0].strip()
                gjjl = re.findall('跟进记录(.*?)进展阶段', xmgk_info_list, re.S)[0].strip()
                jzjd = re.findall('进展阶段(.*?)项目性质', xmgk_info_list, re.S)[0].strip()
                xmxz = re.findall('项目性质(.*?)业主类型', xmgk_info_list, re.S)[0].strip()
                yzlx = re.findall('业主类型(.*?)项目类别', xmgk_info_list, re.S)[0].strip()
                xmlb = re.findall('项目类别(.*?)项目子类别', xmgk_info_list, re.S)[0].strip()
                xmzlb = re.findall('项目子类别(.*?)项目投资', xmgk_info_list, re.S)[0].strip()
                xmtz = re.findall('项目投资(.*?)开工时间', xmgk_info_list, re.S)[0].strip()
                kgsj = re.findall('开工时间(.*?)竣工时间', xmgk_info_list, re.S)[0].strip()
                jgsj = re.findall('竣工时间(.*?)建筑面积', xmgk_info_list, re.S)[0].strip()
                jzmj = re.findall('建筑面积(.*?)占地面积', xmgk_info_list, re.S)[0].strip()
                zdmj = re.findall('占地面积(.*?)建筑物层数', xmgk_info_list, re.S)[0].strip()
                jzwcs = re.findall('建筑物层数(.*?)钢结构', xmgk_info_list, re.S)[0].strip()
                gjg = re.findall('钢结构(.*?)装修情况', xmgk_info_list, re.S)[0].strip()
                zxqk = re.findall('装修情况(.*?)装修标准', xmgk_info_list, re.S)[0].strip()
                zxbz = re.findall('装修标准(.*?)外墙预算', xmgk_info_list, re.S)[0].strip()
                wqys = re.findall('外墙预算(.*?)项目概况', xmgk_info_list, re.S)[0].strip()
                gk = re.findall('项目概况\n(.*?)\n\n', xmgk_info_list, re.S)[0].strip()
                QLM_xmgk = [
                    {'项目编号': xmbh, '跟进记录': gjjl, '进展阶段': jzjd, '项目性质': xmxz, '业主类型': yzlx, '项目类别': xmlb, '项目子类别': xmzlb,
                     '项目投资': xmtz, '开工时间': kgsj, '竣工时间': jgsj, '建筑面积': jzmj, '占地面积': zdmj, '建筑物层数': jzwcs, '钢结构': gjg,
                     '装修情况': zxqk, '装修标准': zxbz, '外墙预算': wqys, '项目概况': gk}]
                # print(QLM_xmgk)

                # 项目联系人：
                xmlxr_info_list = soup.select('div.zhengC > table')[2]
                QLM_xmlxr = []
                xmlxr_group_list = str(xmlxr_info_list).split('text-align: ')
                for xmllxr_i in range(1, len(xmlxr_group_list)):
                    contact_list = []
                    c_Type = re.findall('center;">(.*?)</td>', xmlxr_group_list[xmllxr_i], re.S)[0]

                    dwmc = re.findall('单位名称：</td>\n<td>(.*?)</td>', xmlxr_group_list[xmllxr_i], re.S)
                    try:
                        lxr = re.findall('联 系 人：</td>\n<td>(.*?)<input', xmlxr_group_list[xmllxr_i], re.S)
                    except:
                        lxr = ' '
                    try:
                        tel = re.findall('电    话：</td>\n<td>(.*?)</td>', xmlxr_group_list[xmllxr_i], re.S)
                    except:
                        tel = ' '
                    try:
                        phone = re.findall('手    机：</td>\n<td>(.*?)</td>', xmlxr_group_list[xmllxr_i], re.S)
                    except:
                        phone = ' '
                    try:
                        address = re.findall('地    址：</td>\n<td>(.*?)</td>', xmlxr_group_list[xmllxr_i], re.S)
                    except:
                        address = ' '

                    for i in range(len(dwmc)):
                        contact_list.append({'单位名称': dwmc[i].strip(), '联系人': lxr[i].strip(), '电话': tel[i].strip(),
                                             '手机': phone[i].strip(), '地址': address[i].strip()})
                        # print(dwmc[i],lxr[i],tel[i],phone[i],address[i])
                    QLM_xmlxr.append({'section': c_Type, 'contact_list': contact_list})

                try:
                    insert_sql = "INSERT INTO `qianlima_good`(project_name,project_area,project_updateT,project_showT,project_xmgj,project_xmgk,project_contact,crap_time) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(project_name, project_area, update_Time, fbsj, json.dumps(QLM_xmgj, ensure_ascii=False),json.dumps(QLM_xmgk, ensure_ascii=False), json.dumps(QLM_xmlxr, ensure_ascii=False), lfTime)
                    # insert_sql = "INSERT INTO `QianLiMa_Normal`(project_name,project_area,project_updateT,project_showT,project_xmgj,project_xmgk,project_contact,crap_time) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(project_name,project_area,update_Time,fbsj,json.dumps(QLM_xmgj,ensure_ascii=False),json.dumps(QLM_xmgk,ensure_ascii=False),json.dumps(QLM_xmlxr,ensure_ascii=False),lfTime)

                    cursor.execute(insert_sql)
                    db.commit()
                    print(project_name, ' -insert')
                except Exception as e:
                    db.rollback()
                    print('db-', e)
            except Exception as e:
                print('lalala', project_url, e)
    db.close()
    cursor.close()


save_data_inDB()
# save_vip_url_handle()
# save_url_info()
