import requests,random,pymysql,re,time
from bs4 import BeautifulSoup
import http.cookiejar
from multiprocessing import Pool,Lock
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains

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
    proxies = {
        'http':'http://'+random.choice(proxies_list)
    }
    return proxies

def get_headers(referer):
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
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    ]
    headers = {
        'User-Agent':random.choice(USER_AGENTS),
        'Host':'hm.baidu.com',
        'Referer':referer,
    }
    return headers

def handle():
    global lock,cate_all_url,error_file
    lock = Lock()
    cate_all_url = open('company_all_info.csv','w')
    error_file = open('error_file.csv','w')

    info_tuple_list = []
    # with open('company_all_url.csv','r') as cate_url_file:
    with open('error_file1.csv','r') as cate_url_file:
        for cate_url in cate_url_file.readlines():
            firs_cate = cate_url.split(',')[0]
            sec_cate = cate_url.split(',')[1]
            company_titel = cate_url.split(',')[2].strip()
            company_url = cate_url.split(',')[3].strip()
            # print(firs_cate,sec_cate,basic_url)
            info_tuple_list.append((firs_cate,sec_cate,company_titel,company_url))

    pool = Pool(30)
    pool.map(get_info,info_tuple_list)
    pool.close()
    pool.join()
    cate_all_url.close()
    error_file.close()

def get_info(info_list):
    firs_cate = info_list[0]
    sec_cate = info_list[1]
    company_titel = info_list[2]
    company_url = info_list[3]
    try:
        # ss=get_proxies_ip()
        time.sleep(5)
        req = requests.get(company_url,headers=get_headers(company_url),proxies=get_proxies_ip(),timeout=60)
        req.encoding = 'gb2312'
        soup = BeautifulSoup(req.text,'html.parser')
        company_info = str(soup.select('body > div.top3 > div > div.top3left > div > div')[0])
        try:
            company_address = re.findall('所在地址：(.*?)<br/>',company_info,re.S)[0].strip()
        except:
            company_address = ''
        try:
            company_tel = re.findall('联系电话：(.*?)<br/>',company_info,re.S)[0].strip()
        except:
            company_tel = ''
        try:
            company_phone = re.findall('手　　机：(.*?)<br/>',company_info,re.S)[0].strip()
        except:
            company_phone = ''
        try:
            company_contact = re.findall('联 系 人：(.*?)</span>',company_info,re.S)[0].strip()
        except:
            company_contact = ''
        try:
            company_major = '、'.join(re.findall('<u>(.*?)</u>',company_info,re.S)).strip()
        except:
            company_major = ''
        try:
            company_bussiness = '、'.join(re.findall('主营业务：(.*?)</div>',company_info,re.S)).strip()
        except:
            company_bussiness = ''
        # print(company_titel+','+company_address+','+company_tel+','+company_phone+','+company_contact+','+company_major+','+company_bussiness+'\n')
        lock.acquire()
        cate_all_url.write(firs_cate+','+sec_cate+','+company_titel+','+company_address+','+company_tel+','+company_phone+','+company_contact+','+company_major+','+company_bussiness+'\n')
        cate_all_url.flush()
        lock.release()
        print(company_titel)

    except Exception as e:
        lock.acquire()
        error_file.write(firs_cate+','+sec_cate+','+company_titel+','+company_url+'\n')
        error_file.flush()
        lock.release()
        # print(req.text)
        print(company_url)

handle()


def use_phonetomJS():
    PROXY = get_proxies_ip()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server={0}'.format(PROXY))
    # driver = webdriver.PhantomJS(executable_path='/Users/Dery/SeleniumWebDriver/phantomjs-2.1.1-macosx/bin/phantomjs',service_args=service_args, desired_capabilities=dcap)

    cate_all_url = open('company_all_info.csv','w')
    error_file = open('error_file1.csv','w')
    driver = webdriver.Chrome(executable_path='/Users/Dery/SeleniumWebDriver/chromedriver',chrome_options=chrome_options)

    with open('error_file.csv','r') as cate_url_file:
        for cate_url in cate_url_file.readlines():
            firs_cate = cate_url.split(',')[0]
            sec_cate = cate_url.split(',')[1]
            company_titel = cate_url.split(',')[2].strip()
            company_url = cate_url.split(',')[3].strip()
            # print(firs_cate,sec_cate,basic_url)
            driver.get(company_url)
            js10=["document.body.scrollTop={}".format(100*i) for i in range(15)]
            for js in js10:
                time.sleep(0.8)
                driver.execute_script(js)
            try:
                soup = BeautifulSoup(driver.page_source,'html.parser')
                company_info = str(soup.select('body > div.top3 > div > div.top3left > div > div')[0])
                try:
                    company_address = re.findall('所在地址：(.*?)<br/>',company_info,re.S)[0].strip()
                except:
                    company_address = ''
                try:
                    company_tel = re.findall('联系电话：(.*?)<br/>',company_info,re.S)[0].strip()
                except:
                    company_tel = ''
                try:
                    company_phone = re.findall('手　　机：(.*?)<br/>',company_info,re.S)[0].strip()
                except:
                    company_phone = ''
                try:
                    company_contact = re.findall('联 系 人：(.*?)</span>',company_info,re.S)[0].strip()
                except:
                    company_contact = ''
                try:
                    company_major = '、'.join(re.findall('<u>(.*?)</u>',company_info,re.S)).strip()
                except:
                    company_major = ''
                try:
                    company_bussiness = '、'.join(re.findall('主营业务：(.*?)</div>',company_info,re.S)).strip()
                except:
                    company_bussiness = ''
                # print(company_titel+','+company_address+','+company_tel+','+company_phone+','+company_contact+','+company_major+','+company_bussiness+'\n')
                cate_all_url.write(firs_cate+','+sec_cate+','+company_titel+','+company_address+','+company_tel+','+company_phone+','+company_contact+','+company_major+','+company_bussiness+'\n')
                cate_all_url.flush()
                print(company_titel)

            except Exception as e:
                error_file.write(firs_cate+','+sec_cate+','+company_titel+','+company_url+'\n')
                error_file.flush()
                # print(req.text)
                print(company_url)
