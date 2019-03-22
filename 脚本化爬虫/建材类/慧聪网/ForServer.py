from bs4 import BeautifulSoup
import time,pymysql
import requests,re,random,json
from multiprocessing import Lock,Pool

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

def get_product_url_handle():
    global lock,error_file,company_product_url
    company_product_url = open('company_product_url_0531.csv','w')
    error_file = open('error_file_0531.csv','w')
    lock = Lock()
    info_tuple = []
    Company_prouct_page = open('XXXXXXXXX.csv','r')
    for Company_prouct in Company_prouct_page.readlines():
        first_cate,second_cate,company_url,company_name = Company_prouct.split(',')
        # print(first_cate,second_cate,company_url,company_name)
        info_tuple.append((first_cate,second_cate,company_url,company_name.strip()))


def get_product_url(info_tuple):
    first_cate,second_cate,company_url,company_name = info_tuple
    try:
        # responseLF = requests.get(company_url,headers=get_headers(),proxies=get_proxies_ip())
        responseLF = requests.get(company_url,headers=get_headers())
        soup = BeautifulSoup(responseLF.text,'html.parser')
        cate_info = {'cate_info':''.join([i.text.replace('\n','').replace('\t','').replace('全部','').replace('\r','').replace(',','').strip() for i in soup.select('#mainContList')])}
        product_info =  soup.select('div.ProlistCont > div.ListModMain > div.itemListMod > ul > li > dl > dt > a')
        price_info = soup.select('div.ProlistCont > div.ListModMain > div.itemListMod > ul > li > dl > dd.itemPrice')
        for i in range(len(product_info)):
            product_url,product_name,price = product_info[i]['href'],product_info[i]['title'],price_info[i].text
            company_product_url.write(first_cate+','+second_cate+','+company_url+','+company_name.strip().replace(',','')+','+json.dumps(cate_info,ensure_ascii=False)+','+product_url+','+product_name.replace(',','')+','+price+'\n')
            company_product_url.flush()
            print(product_name)
    except Exception as e:
        error_file.write(first_cate+','+second_cate+','+company_url+','+company_name)
        error_file.flush()
        print(e,company_url)


def get_product_info_handle():
    global lock,error_file,HCdb,HCcursor
    lock = Lock()
    # HCdb = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    HCdb = pymysql.connect("192.168.1.231","root","3jw9lketj0","ConstructionMaterials",charset='utf8')
    HCcursor = HCdb.cursor()

    info_tuple = []
    # company_product_url = open('company_product_url_0607.csv','r')
    company_product_url = open('error_file_0614.csv','r')
    error_file = open('error_file_0616.csv','w')
    for Company_prouct in company_product_url.readlines():
        try:
            first_cate,second_cate,company_url,company_name,cate_info,product_url,product_name,product_prict = Company_prouct.split(',')
            info_tuple.append((first_cate,second_cate,company_url,company_name,cate_info,product_url,product_name,product_prict.strip()))
        except:
            pass
    pool = Pool(10)
    pool.map(get_product_info,info_tuple)
    pool.close()
    pool.join()
    error_file.close()
    HCdb.close()
    HCcursor.close()

def get_product_info(info_tuple):

    first_cate,second_cate,company_url,company_name,cate_info,product_url,product_name,product_price = info_tuple
    try:
        HC_response = requests.get(product_url,headers=get_headers(),timeout=5,proxies=get_proxies_ip())
        time.sleep(0.3)
        HC_response.encoding = 'gbk'
        soup = BeautifulSoup(HC_response.text,'html.parser')
        try:
            img_list = ' '.join(i['src'].replace('100x100','600x600') for i in soup.select('#thumblist > li > div > a > img'))
        except:
            img_list = ' '
        try:
            product_area = soup.select('div.item-mmt-txt > ul > li > div > p')[0].text
        except:
            product_area = ' '
        try:
            basic_data = ' '.join(i.text.replace('\n','').replace('\t','').replace('  ','').replace('同参数产品',' ').replace('\r','').strip() for i in soup.select('#pdetail > div.d-vopy > table'))
        except:
            basic_data = ' '
        try:
            insert_sql = "INSERT INTO `HUiCong_Product`(first_cate,second_cate,company_url,company_name,cate_info,product_name,product_url,product_price,product_img,product_area,canshu) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(first_cate,second_cate,company_url,company_name,cate_info,product_name,product_url,product_price,img_list,product_area,basic_data)
            HCcursor.execute(insert_sql)
            HCdb.commit()
            print(product_name,' -insert')
        except Exception as e:
            HCdb.rollback()
            print('db-',e)
    except:
        lock.acquire()
        error_file.write(first_cate+','+second_cate+','+company_url+','+company_name+','+cate_info+','+product_url+','+product_name+','+product_price+'\n')
        error_file.flush()
        lock.release()

get_product_info_handle()


