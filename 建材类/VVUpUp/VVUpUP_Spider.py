from bs4 import BeautifulSoup
import requests,pymysql
import random,re,json
from multiprocessing import Pool,Lock

'http://www.vvupup.com'
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

# 存储分类及三级分类的url
def write_cate_url():
    teVVUPUP =  open('teVVUPUP.html','r')
    with open('cate_url.csv','w') as xxxxx:
        soup = BeautifulSoup(teVVUPUP.read(),'html.parser')

        for i in range(1,5):
            print(soup.select('div.parent-category > img')[i]['alt'])
            frirst = soup.select('div.parent-category > img')[i]['alt']

            second = soup.select('div.home-channel > div > div:nth-of-type({}) > div.expand-panel > div.expand-category > div > div > div.parent-name > strong > span > a'.format(i))
            for se in range(len(second)):
                print(second[se].text)
                thrid = soup.select('div.home-channel > div > div:nth-of-type({}) > div.expand-panel > div.expand-category > div > div:nth-of-type({}) > div.children-name > div > a'.format(i,se+1))

                for th in thrid:
                    print(th['href'],th.text)
                    xxxxx.write(frirst+','+second[se].text+','+th.text+','+th['href']+'\n')

# 获取所有的产品url
def save_all_product_handle():
    global lock,error_file,UpUp_product_url
    lock = Lock()
    error_file = open('error_file.csv','w')
    UpUp_product_url = open('UpUp_product_url1.csv','w')
    UpUp_page = open('UpUp_page.csv','r')
    info_list = []
    # 获取所有的产品url
    for info_i in UpUp_page.readlines():
        # first_cate,second_cate,third_cate,third_url,page_num = info_i.split(',')
        first_cate,second_cate,third_cate,third_url = info_i.split(',')
        # if eval(page_num) == 1:
        #     info_list.append((first_cate,second_cate,third_cate,third_url))
        # else:
        #     for requests_url in [third_url.strip()+'&pageNo={}&pageSize=20'.format(i) for i in range(2,eval(page_num)+1)]:
        #         info_list.append((first_cate,second_cate,third_cate,requests_url))
        info_list.append((first_cate,second_cate,third_cate,third_url))

    pool = Pool(20)
    pool.map(save_all_product_url,info_list)
    pool.close()
    pool.join()
    error_file.close()
    UpUp_product_url.close()

def save_all_product_url(info_list):
    first_cate = info_list[0]
    second_cate = info_list[1]
    third_cate = info_list[2]
    requests_url = info_list[3]
    # print(first_cate,second_cate,third_cate,requests_url)
    try:
        response = requests.get(requests_url.strip(),headers=get_headers(),proxies=get_proxies_ip(),timeout=80)
        soup = BeautifulSoup(response.text,'html.parser')
        for i in soup.select('div.list > ul > li > div > a'):
            lock.acquire()
            UpUp_product_url.write(first_cate+','+second_cate+','+third_cate+','+i.img['alt']+','+'http://www.vvupup.com'+i['href']+'\n')
            UpUp_product_url.flush()
            lock.release()
            print(i.img['alt'])

    except Exception as e:
        lock.acquire()
        error_file.write(first_cate+','+second_cate+','+third_cate+','+requests_url.strip()+'\n')
        error_file.flush()
        lock.release()
        print(e)


# 把数据存到数据库
def get_pic_info_handle():
    global lock,error_file
    lock = Lock()
    error_file = open('error_file.csv','w')
    UpUp_product_url = open('UpUp_product_url.csv','r')
    info_list = []
    for info_i in UpUp_product_url.readlines():

        first_cate = info_i.split(',')[0]
        second_cate = info_i.split(',')[1]
        third_cate = info_i.split(',')[2]
        product_name = ' '.join(info_i.split(',')[3:-1])
        product_url = info_i.split(',')[-1]
        info_list.append((first_cate,second_cate,third_cate,product_name,product_url.strip()))
    # print(info_list)
    pool = Pool(20)
    pool.map(get_pic_info_saveDB,info_list)
    pool.close()
    pool.join()

    error_file.close()

def get_pic_info_saveDB(info_list):
    db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    cursor = db.cursor()

    first_cate = info_list[0]
    second_cate = info_list[1]
    third_cate = info_list[2]
    product_name = info_list[3]
    product_url = info_list[4]

    try:
        response = requests.get(product_url,headers=get_headers(),proxies=get_proxies_ip(),timeout=80)
        soup = BeautifulSoup(response.text,'html.parser')

        company_name = soup.select('dd > strong')[0].text

        sup_info_list = []
        for info_text in soup.select('ul.spu-info'):
            sup_info_list.append(info_text.text.strip().replace('   ','').replace('\n',' '))
            # print('')
        sup_info = ''.join(sup_info_list)
        try:
            img_list = json.dumps(re.findall('src="(.*?)"',str(soup.select('div.tab-content > img')[0]),re.S))
        except:
            img_list = ' '
        img_info = json.dumps(re.findall('src="(.*?)"',str(soup.select('ul.images')),re.S))

        insert_sql= "INSERT INTO `VVUpUp`(up_first_cate,up_second_cate,up_third_cate,up_company_name,up_product_name,up_info,up_img_list,up_intro_img) VALUES('{}','{}','{}','{}','{}','{}','{}','{}');".format(first_cate,second_cate,third_cate,company_name,product_name,sup_info,img_list,img_info)
        try:
            cursor.execute(insert_sql)
            db.commit()
            print(product_name,'insert')
        except:
            db.rollback()
            print('db-error')
    except Exception as e:
        lock.acquire()
        error_file.write(first_cate+','+second_cate+','+third_cate+','+product_name+','+product_url+'\n')
        error_file.flush()
        lock.release()
        print(product_url,e)



if __name__ == '__main__':
    get_pic_info_handle()