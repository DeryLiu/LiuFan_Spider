from bs4 import BeautifulSoup
import time
from multiprocessing import Pool,Lock
from selenium import webdriver
import requests,re,random
import http.cookiejar

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
    # return random.choice(proxies_list)
    return proxies

def get_info_by_phontomJS():
    driver = webdriver.Chrome(executable_path='/Users/Dery/SeleniumWebDriver/chromedriver')
    driver.get('http://pass.buildnet.cn/auth/greennkit')
    # driver.save_screenshot('./data/login_picture1.png')
    code_num = input('please input code:')
    # phantomJS
    driver.find_element_by_id('user').clear()
    driver.find_element_by_id('user').send_keys('mhmt')
    driver.find_element_by_id('pwd').clear()
    driver.find_element_by_id('pwd').send_keys('43ec371b')
    driver.find_element_by_id('txtVCode').send_keys(code_num)
    driver.find_element_by_id("chk1").click()
    driver.find_element_by_xpath('/html/body/div[3]/div[2]/form/ul/li[5]/input').click()
    time.sleep(5)
    print(driver.get_cookies())
    all_category_url = open('./data/all_category_info.csv','r')
    error_file = open('./data/error.csv','w')
    category_cam_list = []
    with open('./data/company_info_data.csv','w') as all_category_info_all:
        for all_category in all_category_url.readlines():
            first_name = all_category.split('\t')[0]
            second_name = all_category.split('\t')[1]
            third_name = all_category.split('\t')[2]
            cate_url = all_category.split('\t')[3]
            campany_name = all_category.split('\t')[4].strip()
            campany_url = all_category.split('\t')[5].strip()
            #--------------------
            try:
                # print(campany_url)
                driver.get(campany_url)
                time.sleep(0.5)
                soup = BeautifulSoup(driver.page_source,'html.parser')
                address = soup.select('#contenl > div.c.basInf > dl > dd:nth-of-type(1) > p')[0].text.strip()
                phone = soup.select('#contenl > div.c.basInf > dl > dd:nth-of-type(2) > p')[0].text.strip()
                all_category_info_all.write(first_name+'\t'+second_name+'\t'+third_name+'\t'+cate_url+'\t'+campany_name+'\t'+campany_url+'\t'+address+'\t'+phone+'\n')
                all_category_info_all.flush()
                print(address)
            except Exception as e:
                error_file.write(first_name+'\t'+second_name+'\t'+third_name+'\t'+cate_url+'\t'+campany_name+'\t'+campany_url+'\n')
                error_file.flush()
                print(e)
        #     driver.quit()


# requests 测试
def handle():
    global lock,all_category_info_all,session,error_file

    lock = Lock()

    error_file = open('./data/error.csv','w')
    all_category_info_all =  open('./data/company_info_data.csv','w')

    login_url = 'http://pass.buildnet.cn/auth/greennkit'
    login_data = {
        'txtUserName':'mhmt',
        'txtUserPassword':'43ec371b',
        'vCode':'135bn',
        'isLoginAnyway':1,
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



    info_tuple = []
    with open('./data/all_category_info.csv','r') as all_category_url:
        for all_category in all_category_url.readlines():
            first_name = all_category.split('\t')[0]
            second_name = all_category.split('\t')[1]
            third_name = all_category.split('\t')[2]
            cate_url = all_category.split('\t')[3]
            campany_name = all_category.split('\t')[4].strip()
            campany_url = all_category.split('\t')[5].strip()

    pool = Pool(20)
    pool.map(get_company_url,info_list_tuple)
    pool.close()
    pool.join()
    GuangCai_Company_file.close()
    error_file.close()

def get_all_url(info_tuple_list):
    city_name = info_tuple_list[0]
    company_name = info_tuple_list[1]
    company_url = info_tuple_list[2]
    # print(city_name,city_main_url)
    try:
        req = requests.get(company_url)
        req.encoding = 'gb2312'
        soup = BeautifulSoup(req.text,'html.parser')
        company_info_list = str(soup.select('#mainLeft > div.contact > ul li'))
        info_list = re.findall('<li>(.*?)</li>',company_info_list,re.S)
        company_contact,company_address,company_tel,company_phone = '','','',''
        main_major = '&'.join(soup.select('#mainRight > div.conA.info > ul > li')[-1].span.text)
        for info in info_list:
            if '联 系 人：' in info:
                company_contact = re.findall('<span>(.*?)</span>',info,re.S)[0]
                # print(company_contact)
            if '公司地址：' in info:
                company_address = re.findall('<span>(.*?)</span>',info,re.S)[0]
                # print(company_address)
            if '公司电话：' in info:
                company_tel = re.findall('<span>(.*?)</span>',info,re.S)[0].split(' ')[0].strip()+'-'+re.findall('<span>(.*?)</span>',info,re.S)[0].split(' ')[-1]
                # print(company_tel)
            if '手 机：' in info:
                company_phone = re.findall('<span>(.*?)</span>',info,re.S)[0]

        lock.acquire()
        company_info_file.write(city_name+','+company_name+','+company_contact+','+company_phone+','+company_tel+','+company_address+','+main_major+'\n')
        company_info_file.flush()
        lock.release()
        print(company_contact)

    except Exception as e:
        lock.acquire()
        error_file.write(city_name+','+company_name+','+company_url+'\n')
        error_file.flush()
        lock.release()
        print(e)



get_info_by_phontomJS()