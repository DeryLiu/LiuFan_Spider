import requests,re,random,pymysql
from bs4 import BeautifulSoup
from multiprocessing import Pool,Lock

def get_proxies_ip():
    # MAX_RETRIES = 20
    # session = requests.Session()
    # adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
    # session.mount('https://', adapter)
    # session.mount('http://', adapter)
    # rp = session.get(url)
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
    return proxies

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

def handle():
    global lock,error_file
    lock = Lock()
    error_file = open('error.csv','w')
    info_tuple_list = []
    url_info = [("http://diban.chinabm.cn/dianping/{}/","地板","536"),("http://chugui.chinabm.cn/dianping/{}/","橱柜","438"),
            ("http://menchuang.chinabm.cn/dianping/{}/","门窗","502"),("http://yigui.chinabm.cn/dianping/{}/","衣柜","392"),
            ("http://weiyu.chinabm.cn/dianping/{}/","卫浴","527"),("http://jingshuiqi.chinabm.cn/dianping/{}/","净水器","140"),
            ("http://shicai.chinabm.cn/dianping/{}/","石材","138"),("http://diaoding.chinabm.cn/dianping/{}/","吊顶","351"),
            ("http://guizaoni.chinabm.cn/dianping/{}/","硅藻泥","133"),("http://taoci.chinabm.cn/dianping/{}/","陶瓷","155"),
            ("http://dengshi.chinabm.cn/dianping/{}/","灯饰","134"),("http://zmjz.chinabm.cn/dianping/{}/","整木","141"),
            ("http://suoju.chinabm.cn/dianping/{}/","锁具","133"),("http://ditan.chinabm.cn/dianping/{}/","地毯","130"),
            ("http://gybl.chinabm.cn/dianping/{}/","玻璃","133"),("http://louti.chinabm.cn/dianping/{}/","楼梯","148"),
            ("http://tuliao.chinabm.cn/dianping/{}/","涂料","150"),("http://qzbb.chinabm.cn/dianping/{}/","墙纸","133"),
            ("http://jjsp.chinabm.cn/dianping/{}/","家饰","147"),("http://jiadian.chinabm.cn/dianping/{}/","家电","124"),
            ("http://cainuan.chinabm.cn/dianping/{}/","采暖","171"),("http://jcz.chinabm.cn/dianping/{}/","集成灶","261"),
            ("http://jiafang.chinabm.cn/dianping/{}/","家纺","135"),("http://wujin.chinabm.cn/dianping/{}/","五金","139"),
            ("http://youqi.chinabm.cn/dianping/{}/","油漆","138"),("http://clby.chinabm.cn/dianping/{}/","窗帘","130"),
            ("http://muye.chinabm.cn/dianping/{}/","木业","144"),("http://cpjj.chinabm.cn/dianping/{}/","家具","131"),
            ("http://zhinengjj.chinabm.cn/dianping/{}/","智家居","120")]
    for basic_info in url_info:
        first_cate = basic_info[1]
        for url in [ basic_info[0].format(i) for i in range(1,int(basic_info[2])+1)]:
            info_tuple_list.append((first_cate,url))

    pool = Pool(20)
    pool.map(get_info,info_tuple_list)
    pool.close()
    pool.join()
    error_file.close()

def get_info(info_tuple_list):
# def get_info(cate,basic_url):
    db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    cursor=db.cursor()
    cate = info_tuple_list[0]
    basic_url = info_tuple_list[1]
    try:
        req = requests.get(basic_url,headers=get_headers(),proxies=get_proxies_ip(),timeout=50)
        soup = BeautifulSoup(req.text,'html.parser')
        all_comments = soup.select('body > div.w1190.wauto > div.fl.w820 > div.n_comments dl')
        for comments in all_comments:
            commenter = comments.span.text
            product_name = comments.a.text.strip("怎么样")
            comment_type = comments.i.text.strip("(").split(")")[0]
            comments_info = comments.dd.text
            comment_time = re.findall('<span class="fr f_gray">(.*?)</span>',str(comments),re.S)[0]
            if "小时" in comment_time:
                comment_time = '4-18'
            # print(cate,commenter,product_name,comment_type,comments_info,comment_time)
            try:
                insert_sql = "INSERT INTO `ZhongHua_JianCai`(cate,commenter,product,commit_type,comment_info,comment_time) VALUES ('{}','{}','{}','{}','{}','{}');".format(cate,commenter,product_name,comment_type,comments_info,comment_time)
                cursor.execute(insert_sql)
                db.commit()
                print(commenter,' -insert')
            except Exception as e:
                db.rollback()
                print('db-',e)

    except Exception as e:
        lock.acquire()
        error_file.write(cate+','+basic_url+'\n')
        error_file.flush()
        lock.release()
        print(cate+','+basic_url)
        print(e)

    cursor.close()
    db.close()


handle()

# with open('error.csv','r') as error_file:
#     for basic_info in error_file.readlines():
#         cate,url = basic_info.split(',')
#         get_info(cate,url.strip())
