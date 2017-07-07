from bs4 import BeautifulSoup
import requests,pymysql,random,time
import http.cookiejar
from multiprocessing import Pool,Lock

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
    porxite = {
        'http':'http://'+random.choice(proxies_list)
    }
    return porxite

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
    return random.choice(USER_AGENTS)

def handle():
    global lock,session,GuangCai_Company_file
    lock = Lock()
    GuangCai_Company_file = open('GuangCai_Company_info.csv','w')
    headers= {'User-Agent': get_headers(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Host':'www.gldjc.com',
        'Origin':'http://www.gldjc.com',
        'Referer':'http://www.gldjc.com/login?hostUrl=http://www.gldjc.com/membercenter/toRenewOrderPage'}

    login_data = {
        'userName':'13105279055',
        'password':'gld123456'
    }
    login_url = 'http://www.gldjc.com/dologin'

    # 建立一个会话，可以把同一用户的不同请求联系起来；直到会话结束都会自动处理cookies
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

    content = session.post(login_url,data=login_data,headers=headers)
    # print(content.content)
    # 保存cookie到本地
    session.cookies.save(ignore_discard=True, ignore_expires=True)

    basic_url = ['http://search.gldjc.com/company.action?keyword=&currentPage={}'.format(i+1) for i in range(1475)]
    pool = Pool(5)
    pool.map(get_info,basic_url)
    pool.close()
    pool.join()
    GuangCai_Company_file.close()

def get_info(url):
    time.sleep(1)
    print(url)
    headers = {
        'User-Agent': get_headers(),
        'Host':'search.gldjc.com',
    }
    try:
        req = session.get(url,allow_redirects=False,headers=headers,proxies=get_proxies_ip(),timeout=60)
        req.encoding = 'utf-8'
        # print(req.text)
        soup = BeautifulSoup(req.text,'html.parser')
        # page_count = soup.select('span#totalPageNum')[0].text
        company_info_list = soup.select('tr > td:nth-of-type(6) > ul > dl > div > ul')
        # print(company_info_list)
        for company_info in company_info_list:
            company_name = str(company_info).split('<li>')[1].split('：')[1].split('</li>')[0]
            company_adder = str(company_info).split('<li>')[2].split('：')[1].split('</li>')[0]
            try:
                company_tel = str(company_info).split('<li>')[4].split('：')[1].split('</li>')[0]
            except:
                company_tel = ''
            try:
                company_people = str(company_info).split('<li>')[5].split('：')[1].split('</li>')[0]
            except:
                company_people = ''
            company_id = company_info.a['_href'].split('/')[-1]

            lock.acquire()
            GuangCai_Company_file.write(company_name+'\t'+company_adder+'\t'+company_tel+'\t'+company_people+'\t'+company_id+'\n')
            GuangCai_Company_file.flush()
            # print(company_id)
            lock.release()
            print(company_name,company_adder,company_tel,company_people,company_id)
    except Exception as e:
        lock.acquire()
        with open('error.csv','a') as error_fil:
            error_fil.write(url+'\n')
        lock.release()
        print(e)

handle()