import requests,re,random,pymysql
from bs4 import BeautifulSoup
from multiprocessing import Pool,Lock
# 抓取分类及其url
# with open('text.html','r',encoding='gb2312') as aaaa:
#     soup = BeautifulSoup(aaaa.read(),'html.parser')
#     all_cat_list = soup.select('body > div > div.tjbox_l.h390 > div h2 a')
#     # print(all_cat_list[1].text)
#
#     sec_cate_list = soup.select('div.itemlist > ul > li > h3')
#
#     for i in range(1,4):
#         fir_cate = soup.select('div.tjbox_l.h390 > div:nth-of-type({}) > div.itemcell > h2 > a'.format(i+1))[0].text
#         # print(fir_cate)
#         try:
#             for j in range(1,7):
#                 sec_cate = soup.select('div.tjbox_l.h390 > div:nth-of-type({i}) > div.itemlist > ul > li:nth-of-type({j}) > h3 > a'.format(i=i+1,j=j))[0].text
#                 # print(sec_cate)
#                 thir_cate_list = soup.select('div.tjbox_l.h390 > div:nth-of-type({i}) > div.itemlist > ul > li:nth-of-type({j}) > a'.format(i=i+1,j=j))
#                 for thir_cate in thir_cate_list:
#                     thir_cate_name = thir_cate['title']
#                     thir_cate_url = 'http://www.bmlink.com'+thir_cate['href']
#                     company.write(fir_cate+'\t'+sec_cate+'\t'+thir_cate_name+'\t'+thir_cate_url+'\n')
#                     print(fir_cate,sec_cate,thir_cate_name,thir_cate_url)
#         except Exception as s:
#             print(s)
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
    global lock,company_file,error_file
    lock = Lock()
    # company_file = open('compang_info.csv','w')
    # error_file = open('error_file.csv','w')
    # company_url = open('all_compang_url.csv','r')
    company_file = open('compang_info.csv','w')
    error_file = open('error_file.csv','w')
    company_url = open('error_file1.csv','r')
    info_tuple_list = []
    for comp_url_all in company_url.readlines():
        firt_cate = comp_url_all.split(',')[0]
        sec_cate = comp_url_all.split(',')[1]
        thir_cate = comp_url_all.split(',')[2]
        comp_name = comp_url_all.split(',')[3].strip()
        # comp_url = comp_url.split(',')[4].strip()
        info_tuple_list.append((firt_cate,sec_cate,thir_cate,comp_name))
        # print(firt_cate,sec_cate,thir_cate,comp_list_url)
    pool = Pool(30)
    pool.map(get_info,info_tuple_list)
    pool.close()
    pool.join()
    company_file.close()
    error_file.close()

def get_info(info_tuple_list):
    firt_cate = info_tuple_list[0]
    sec_cate = info_tuple_list[1]
    thir_cate = info_tuple_list[2]
    # company_name = info_tuple_list[3]
    # company_url = info_tuple_list[4]
    company_url = info_tuple_list[3]
    # print(company_url)
    try:
        # req = requests.get(company_url)
        req = requests.get(company_url,headers=get_headers(),proxies=get_proxies_ip(),timeout=50)
        req.encoding = 'gb2312'
        soup = BeautifulSoup(req.text,'html.parser')
        # 获取页数
        # page_count = soup.select('body > div.box.sell > div.box > div')[0].text.split('/')[1].split('页')[0]
        # 获取公司地址
        # company_info_list = soup.select('div > ul > li > a.lxfs')
        # 获取联系方式'
        contact_peop = soup.select('div.card > div.cardName > h3')[0].text
        info_all = str(soup.select('div.card > dl')[0])
        company_name = soup.select('div.leftSider > div > h3')[0].text
        try:
            comp_part = re.findall('部 门：(.*?)<',info_all,re.S)[0]
        except:
            comp_part = ''
        try:
            comp_phone = re.findall('手 机：(.*?)<',info_all,re.S)[0]
        except:
            comp_phone = ''
        try:
            comp_call = re.findall('电  话：(.*?)<',info_all,re.S)[0]
        except:
            comp_call = ''
        try:
            comp_addr = re.findall('地  址：(.*?)<',info_all,re.S)[0]
        except:
            comp_addr = ''

        lock.acquire()
        company_file.write(firt_cate+','+sec_cate+','+thir_cate+','+company_name+','+company_url+','+contact_peop+','+comp_part+','+comp_phone+','+comp_call+','+comp_addr+'\n')
        company_file.flush()
        print(company_name)
        lock.release()
        # for company_info in company_info_list:
        #     company_name = company_info['title']
        #     company_url = company_info['href']
        #     print(company_name,company_url)
        #     lock.acquire()
        #     company_file.write(firt_cate+'\t'+sec_cate+'\t'+thir_cate+'\t'+company_name+'\t'+company_url+'\n')
        #     company_file.flush()
        #     lock.release()
    except Exception as e:
        lock.acquire()
        error_file.write(firt_cate+','+sec_cate+','+thir_cate+','+company_url+'\n')
        error_file.flush()
        lock.release()
        print(company_url)

handle()
#
# with open('text.html','r',encoding='gb2312') as sss:
#     soup = BeautifulSoup(sss.read(),'html.parser')
#     contact_peop = soup.select('div.card > div.cardName > h3')[0].text
#     info_all = str(soup.select('div.card > dl')[0])
#     print(contact_peop,info_all)
#     # try:
#     #     for i in range(1,3):
#     #         dt_list = soup.select('div.card > dl dt:nth-of-type({i})'.format(i))
#     #         dd_list = soup.select('div.card > dl > dd:nth-of-type({i})'.format(i))
#     #         print(dd_list)
#     #         print('-=-=')
#     #         print(dt_list)
#     # except:
#     #     print('nono')
#     info_all = str(soup.select('div.card > dl')[0])
#     try:
#         comp_part = re.findall('部 门：(.*?)<',info_all,re.S)[0]
#     except:
#         comp_part = ''
#     try:
#         comp_phone = re.findall('手 机：(.*?)<',info_all,re.S)[0]
#     except:
#         comp_phone = ''
#     try:
#         comp_call = re.findall('电  话：(.*?)<',info_all,re.S)[0]
#     except:
#         comp_call = ''
#     try:
#         comp_addr = re.findall('地  址：(.*?)<',info_all,re.S)[0]
#     except:
#         comp_addr = ''
#     # comp_part = soup.select('div.card > dl dt:nth-of-type(1)')[0].text.split('部 门：')[1]
#     # comp_phone = soup.select('div.card > dl > dd:nth-of-type(1)')[0].text.split('手 机：')[1]
#     # comp_call = soup.select('div.card > dl dt:nth-of-type(2)')[0].text.split('电  话：')[1]
#     # comp_addr = soup.select('div.card > dl dt:nth-of-type(3)')[0].text.split('地  址：')[1]
#     print(contact_peop+','+comp_part+','+comp_phone+','+comp_call+','+comp_addr)

#     # company_info_list = soup.select('div > ul > li > a.lxfs')
#     # for company_info in company_info_list:
#     #     company_name = company_info['title']
#     #     company_url = company_info['href']
#     #     print(company_name,company_url)
