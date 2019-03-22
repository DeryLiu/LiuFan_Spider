from bs4 import BeautifulSoup
import requests,time,re,random,pymysql
from multiprocessing import Pool,Lock
from selenium import webdriver

'https://search.mycaigou.com/bidding.html'
'https://search.mycaigou.com/bidding.html?page=2'

'明源账号  18917858587 密码Fq123456'
all_page = 466

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
        'User-Agent':random.choice(USER_AGENTS),
    }
    return headers


def text1():
    with open('text.html','r') as text_file:
        soup = BeautifulSoup(text_file.read(),'html.parser')
        projectName_url = soup.select('div.table_info > div.tender_cont > ul > li > div.tender_title > h3 > a')
        for i in range(len(projectName_url)):
            print(projectName_url[i]['href'],projectName_url[i].text)

def text2():
    with open('text.html','r') as text_file:
        soup = BeautifulSoup(text_file.read(),'html.parser')
        project_name = soup.select('#nav-tit > div > h3')[0].text
        project_area = soup.select('#nav-tit > div > div.recutit_meta > ul > li:nth-of-type(1)')[0].text
        server_info = soup.select('#nav-tit > div > div.recutit_meta > ul > li:nth-of-type(2)')[0].text
        resgin_money = soup.select('#nav-tit > div > div.recutit_meta > ul > li:nth-of-type(4)')[0].text
        open_data = soup.select('#nav-tit > div > div.recutit_meta > ul > li:nth-of-type(5)')[0].text
        end_data = soup.select('#nav-tit > div > div.recutit_meta > ul > li:nth-of-type(6)')[0].text
        bidding_area = soup.select('#content > div.con_main > div.area_intro.desc_box > div.bd')[0].text.strip()
        condition = soup.select('#content > div.con_main > div.condition_intro.desc_box > div.bd > p')[0].text.strip()
        bidding_info = soup.select('#content > div.con_main > div.desc_intro.desc_box > div.bd')[0].text.strip()
        logo = soup.select('#content > div.sidebar > div > div.company > img')[0]['src']
        company_name = soup.select('#content > div.sidebar > div > div.company > img')[0]['title']
        No_num = soup.select('#content > div.sidebar > div > div.company_meta > ul > li')[0].text
        company_url = soup.select('#content > div.sidebar > div > div.company_meta > ul > li.no_wrap > a')[0].text
        address = soup.select('#content > div.sidebar > div > div.company_meta > ul > li')[-1].text.strip()
        history_bidding = soup.select('#content > div.sidebar > div > div.count > p > a')[0].text
        history_bidding_url = soup.select('#content > div.sidebar > div > div.count > p > a')[0]['href']
        now_bidding = soup.select('#content > div.sidebar > div > div.count > p > a')[1].text
        now_bidding_url = soup.select('#content > div.sidebar > div > div.count > p > a')[1]['href']
        print(project_name,project_area,server_info,resgin_money,open_data,end_data,bidding_area,condition,bidding_info,logo,company_name)
        print(No_num,company_url,address,history_bidding,history_bidding_url,now_bidding,now_bidding_url)

# text2()

def ipipip():
    # chrome driver 设置代理
    PROXY_IP = get_proxies_ip()
    print(PROXY_IP)
    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server={}".format('111.13.7.116:8080'))
    driver = webdriver.Chrome(executable_path="/Users/Dery/SeleniumWebDriver/chromedriver",chrome_options=options)
    driver.get("http://login.mycaigou.com/")

    # driver.find_element_by_id('J_username').clear()
    # driver.find_element_by_id('J_username').send_keys('18917858587')
    # driver.find_element_by_id('J_password').clear()
    # driver.find_element_by_id('J_password').send_keys('Fq123456')
    # driver.find_element_by_css_selector("#content > div > div.container > div > div.field_main > form > p.buttons > input.btn_login").click()

    time.sleep(360)
    print(driver.get_cookies())

ipipip()
