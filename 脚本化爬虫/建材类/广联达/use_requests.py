from bs4 import BeautifulSoup

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
    r_file = '1.csv'
    w_file = 'w1.csv'
    lock = Lock()
    GuangCai_Company_file = open(w_file,'w')
    headers= {'User-Agent': get_headers(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Host':'www.gldjc.com',
        'Origin':'http://www.gldjc.com',
        'Referer':'http://www.gldjc.com/login?hostUrl=http://www.gldjc.com/membercenter/toRenewOrderPage'}

    login_data = {
        'userName':'13296385392',
        'password':'qazwsxedc'
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
    info_tuple_list = []
    with open(r_file,'r') as GuangCai_file:
        for info in GuangCai_file.readlines():
            firs_cate = info.split('\t')[0].strip()
            secd_cate = info.split('\t')[1].strip()
            thir_cate = info.split('\t')[2].strip()
            cate_url = info.split('\t')[4].strip()
            info_tuple_list.append((firs_cate,secd_cate,thir_cate,cate_url))

    pool = Pool(1)
    pool.map(get_info,info_tuple_list)
    pool.close()
    pool.join()
    GuangCai_Company_file.close()

def get_info(info_tuple_list):
    firs_cate = info_tuple_list[0].strip()
    secd_cate = info_tuple_list[1].strip()
    thir_cate = info_tuple_list[2].strip()
    cate_url = info_tuple_list[3].strip()
    time.sleep(2)
    print(cate_url)
    headers = {
        'User-Agent': get_headers(),
    }
    try:
        req = session.get(cate_url,allow_redirects=False,headers=headers,proxies=get_proxies_ip(),timeout=40)
        req.encoding = 'utf-8'
        # print(req.text)
        soup = BeautifulSoup(req.text,'html.parser')
        # 具体详情页的spu
        for next_page_id in soup.select('#a_checkMore'):
            spu_id = next_page_id['onclick'].split("'")[1]
            lock.acquire()
            GuangCai_Company_file.write(firs_cate+'\t'+secd_cate+'\t'+thir_cate+'\t'+cate_url+'\t'+spu_id+'\n')
            GuangCai_Company_file.flush()
            lock.release()
            print(spu_id)

    except Exception as e:
        lock.acquire()
        with open('error.csv','a') as error_fil:
            error_fil.write(cate_url+'\n')
        lock.release()
        print(e)


handle()

# with open('tehx.html','r') as tehx_file:
#     soup = BeautifulSoup(tehx_file.read(),'html.parser')
#     for next_page_id in soup.select('#a_checkMore'):
#         print(next_page_id['onclick'].split("'")[1])
