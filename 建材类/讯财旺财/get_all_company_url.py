from bs4 import BeautifulSoup
import requests,pymysql,random,time
import http.cookiejar
from multiprocessing import Pool,Lock
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains

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

def get_proxies_ip():
    db = pymysql.connect("localhost","root","xxx","xxx",charset='utf8')
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
    # return random.choice(proxies_list)
    return proxies

# # phontomJs配置
# dcap = dict(DesiredCapabilities.PHANTOMJS)
# dcap["phantomjs.page.settings.userAgent"] = (random.choice(USER_AGENTS))
# dcap["phantomjs.page.settings.resourceTimeout"] = ("1000")
# service_args = [
#     '--proxy='.format(get_proxies_ip())
#     ] #默认为http代理，可以指定proxy type


r_file = 'XCWC_Company_all_page.csv'
w_file = 'XCWC_Company_all_url.csv'

def by_phontomJS():
    PROXY = get_proxies_ip()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server={0}'.format(PROXY))
    # driver = webdriver.PhantomJS(executable_path='/Users/Dery/SeleniumWebDriver/phantomjs-2.1.1-macosx/bin/phantomjs',service_args=service_args, desired_capabilities=dcap)

    GuangCai_Company_file = open(w_file,'w')
    driver = webdriver.Chrome(executable_path='/Users/Dery/SeleniumWebDriver/chromedriver',chrome_options=chrome_options)
    driver.get('http://sso.xuncaiwangcai.com/index.php?r=login')

    # phantomJS
    driver.find_element_by_id('ext1').clear()
    driver.find_element_by_id('ext1').send_keys('13296385392')
    driver.find_element_by_css_selector('#login_form > div > div > div:nth-child(3) > input[type="password"]').clear()
    driver.find_element_by_css_selector('#login_form > div > div > div:nth-child(3) > input[type="password"]').send_keys('qazwsxedc')
    driver.find_element_by_css_selector("#login_form > div > div > div.btn_sub > input").click()
    time.sleep(2)

    with open(r_file,'r') as GuangCai_file:
        for info in GuangCai_file.readlines():
            firs_cate = info.split('\t')[0].strip()
            secd_cate = info.split('\t')[1].strip()
            thir_cate = info.split('\t')[2].strip()
            cate_url = info.split('\t')[4].strip()
            try:
                tiSleep = random.choice([7,8,9,10,11,12,13,14,15,16,17,18,19])
                time.sleep(tiSleep)
                driver.get(cate_url)
                js10=["document.body.scrollTop={}".format(100*i) for i in range(10)]
                for js in js10:
                    time.sleep(0.7)
                    driver.execute_script(js)

                soup = BeautifulSoup(driver.page_source,'html.parser')
                # 具体公司地址
                if cate_url.split('=')[-1].strip()==str(1):
                    company_url_list = soup.select('#content > div.main > div.w.busi_supp_list_list > div.mc > ul > li > div.btn > a.btn_login.btn_login_in')
                else:
                    company_url_list = soup.select('#content > div.main > div.w.busi_supp_list_list > div.mc > ul > li > div.btn > a')

                for company_url in company_url_list:
                    com_url = company_url['wcsid']
                    GuangCai_Company_file.write(firs_cate+'\t'+secd_cate+'\t'+thir_cate+'\t'+cate_url+'\t'+com_url+'\n')
                    GuangCai_Company_file.flush()
                    print(com_url)
                # next_page = driver.find_element_by_css_selector("#a_checkMore")
                # ActionChains(driver).click(next_page).perform()
            except Exception as s:
                with open('error1.csv','a') as error_file:
                    error_file.write(firs_cate+'\t'+secd_cate+'\t'+thir_cate+'\t'+cate_url+'\n')
                    error_file.flush()
                # driver.close()
                print(s)

def handle():
    global lock,GuangCai_Company_file,session,error_file

    lock = Lock()
    error_file = open('error1.csv','w')
    GuangCai_Company_file = open('XCWC_Company_all_url.csv','w')
    login_url = 'http://sso.xuncaiwangcai.com/index.php?r=login'
    login_data = {
        'returnurl':'',
        'rme':0,
        'username':'13105279055',
        'password':'gld123456'
    }
    session = requests.Session()
    filename = 'cookie'
    # 建立LWPCookieJar实例，可以存Set-Cookie3类型的文件。
    # 而MozillaCookieJar类是存为'/.txt'格式的文件
    session.cookies = http.cookiejar.LWPCookieJar(filename)
    # 若本地有cookie则不用再post数据了
    try:
        session.cookies.load(filename=filename, ignore_discard=True)
    except:
        print('Cookie未加载！')

    content = session.post(login_url,data=login_data,headers={'User-Agent':random.choice(USER_AGENTS)})
    # print(content.content)
    # 保存cookie到本地
    session.cookies.save(ignore_discard=True, ignore_expires=True)

    # url = 'http://www.wangcaichina.com/?r=company/search&cate_id=45&page=76'
    # req = session.get(url,headers={'User-Agent':random.choice(USER_AGENTS)})
    # print(req.text)
    info_list_tuple = []
    # with open('XCWC_Company_all_page.csv','r') as GuangCai_file:

    with open('error.csv','r') as GuangCai_file:
        for info in GuangCai_file.readlines():
            try:
                firs_cate = info.split('\t')[0].strip()
                secd_cate = info.split('\t')[1].strip()
                thir_cate = info.split('\t')[2].strip()
                # cate_url = info.split('\t')[4].strip()
                cate_url = info.split('\t')[3].strip()
                info_list_tuple.append((firs_cate,secd_cate,thir_cate,cate_url))
            except:
                print(info)

    pool = Pool(20)
    pool.map(get_company_url,info_list_tuple)
    pool.close()
    pool.join()
    GuangCai_Company_file.close()
    error_file.close()

def get_company_url(info_list):
    firs_cate = info_list[0]
    secd_cate = info_list[1]
    thir_cate = info_list[2]
    cate_url = info_list[3]
    try:
        tiSleep = random.choice([2,3,4,5])
        time.sleep(tiSleep)
        req = session.get(cate_url,headers={'User-Agent':random.choice(USER_AGENTS)},proxies=get_proxies_ip())

        soup = BeautifulSoup(req.text,'html.parser')
        # 具体公司地址
        if cate_url.split('=')[-1].strip()==str(1):
            company_url_list = soup.select('#content > div.main > div.w.busi_supp_list_list > div.mc > ul > li > div.btn > a.btn_login.btn_login_in')
        else:
            company_url_list = soup.select('#content > div.main > div.w.busi_supp_list_list > div.mc > ul > li > div.btn > a')

        for company_url in company_url_list:
            com_url = company_url['wcsid']
            lock.acquire()
            GuangCai_Company_file.write(firs_cate+'\t'+secd_cate+'\t'+thir_cate+'\t'+cate_url+'\t'+com_url+'\n')
            GuangCai_Company_file.flush()
            lock.release()
            print(com_url)
        # next_page = driver.find_element_by_css_selector("#a_checkMore")
        # ActionChains(driver).click(next_page).perform()
    except Exception as s:
        lock.acquire()
        error_file.write(firs_cate+'\t'+secd_cate+'\t'+thir_cate+'\t'+cate_url+'\n')
        error_file.flush()
        lock.release()
        # driver.close()
        print(s)



handle()

# by_phontomJS()