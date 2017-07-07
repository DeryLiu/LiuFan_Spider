'http://www.china-10.com/'

import requests,re,random,pymysql,time,json
from bs4 import BeautifulSoup
from multiprocessing import Pool,Lock

def get_proxies_ip():
    # MAX_RETRIES = 20
    # session = requests.Session()
    # adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
    # session.mount('https://', adapter)
    # session.mount('http://', adapter)
    # rp = session.get(url)
    # db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    db = pymysql.connect("192.168.1.231","root","3jw9lketj0","ConstructionMaterials",charset='utf8')
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

class China10():
    # 获取前十的公司
    def get_Top10_info(self):
        '''
        CREATE TABLE `China10_Top10` (
          `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
          `first_cate` varchar(32) DEFAULT NULL,
          `second_cate` varchar(32) DEFAULT NULL,
          `product` varchar(32) DEFAULT NULL,
          `company` varchar(255) DEFAULT NULL,
          `logo` varchar(255) DEFAULT NULL,
          `rank` varchar(30) DEFAULT NULL,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
        error_file = open('error_file.csv','w')
        db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
        cursor=db.cursor()
        with open('cate_url.csv','r') as cate_url_list_file:
            for cate_url_list in cate_url_list_file.readlines():
                first_cate,second_cate,cate_url = cate_url_list.split(',')
                # print(first_cate,second_cate,cate_url)
                try:
                    req = requests.get(cate_url.strip(),headers=get_headers(),proxies=get_proxies_ip(),timeout=50)
                    soup = BeautifulSoup(req.text,'html.parser')
                    for i in range(1,11):
                        product = soup.select('#top10 > div:nth-of-type({}) > div.brandinfo > dl > dt > a.fl.bname.font16'.format(i*2))[0].text
                        # print(product)
                        logo = soup.select('#top10 > div:nth-of-type({}) > div.brandlogo > a > div > img'.format(i*2))[0]['src']
                        # print(logo)
                        company = soup.select('#top10 > div:nth-of-type({}) > div.brandinfo > dl > dt > a.fl.cname.font16.red'.format(i*2))[0].text.strip('()')
                        # print(company)

                        try:
                            insert_sql = "INSERT INTO `China10_Top10`(first_cate,second_cate,product,company,logo,rank) VALUES ('{}','{}','{}','{}','{}','{}');".format(first_cate,second_cate,product,company,logo,i)
                            cursor.execute(insert_sql)
                            db.commit()
                            print(company,' -insert')
                        except Exception as e:
                            db.rollback()
                            print('db-',e)

                except Exception as e:
                    error_file.write(first_cate+','+second_cate+','+cate_url)
                    error_file.flush()
                    print(e,cate_url)

        cursor.close()
        db.close()

    # 获取网店链接，查找更多公司
    def get_webShop_url(self):
        error_file = open('error_file.csv','w')
        cate_url_list_file = open('cate_url.csv','r')
        with open('company_url.csv','w') as company_url_file:
            for cate_url_list in cate_url_list_file.readlines():
                first_cate,second_cate,cate_url = cate_url_list.split(',')
                # print(first_cate,second_cate,cate_url)
                try:
                    req = requests.get(cate_url.strip(),headers=get_headers(),proxies=get_proxies_ip(),timeout=50)
                    soup = BeautifulSoup(req.text,'html.parser')
                    link = soup.select('div.swiper-container > div > div > div.loadblockmore.font16 > a')
                    company_url = link[1]['href']
                    company_url_file.write(first_cate+','+second_cate+','+company_url+'\n')
                    company_url_file.flush()
                    print(company_url)
                except Exception as e:
                    error_file.write(first_cate+','+second_cate+','+cate_url)
                    error_file.flush()
                    print(e,cate_url)

    # 获取总数
    def get_count_num(self):
        error_file = open('error_file.csv','w')
        cate_url_list_file = open('0000000.csv','r')
        with open('company_url_page.csv','w') as company_url_page:
            for cate_url_list in cate_url_list_file.readlines():
                first_cate,second_cate,cate_url = cate_url_list.split(',')
                # print(first_cate,second_cate,cate_url)
                try:
                    req = requests.get(cate_url.strip(),headers=get_headers(),proxies=get_proxies_ip(),timeout=50)
                    soup = BeautifulSoup(req.text,'html.parser')
                    try:
                        link = soup.select('#rightlay > div.container > div.aclist > div.v2_webshop_col3 > div.loadblockmore.font16 > a')
                        count_num = str(int(int(link[0].text.split('约')[1].split('条')[0])/18)+1)
                    except:
                        count_num = '0'
                    company_url_page.write(first_cate+','+second_cate+','+cate_url.strip()+','+count_num+'\n')
                    print(count_num)
                except Exception as e:
                    error_file.write(first_cate+','+second_cate+','+cate_url)
                    error_file.flush()
                    print(e,cate_url)

    # 获取所有公司网店url
    def get_company_webshop_url_info(self):
        error_file = open('error_file.csv','w')
        cate_url_list_file = open('error_file1.csv','r')
        with open('company_url.csv','w') as company_url_file:
            for cate_url_list in cate_url_list_file.readlines():
                first_cate,second_cate,cate_url,page_num = cate_url_list.split(',')
                try:
                    req_id = cate_url.split('list_')[1].split('.html')[0].strip()
                    for i in range(1,int(page_num.strip())+1):
                        req_url = 'http://www.china-10.com/ajaxstream/?do=loadblock&dataType=text&param=v2_webshop_col3_catid%3A{id_num}_num%3A18_page%3A{add_num}'.format(id_num=req_id,add_num=i)
                        # print(req_url)
                        req = requests.get(req_url,headers=get_headers(),proxies=get_proxies_ip(),timeout=50)
                        url_list = re.findall('<a isconvert=1 target="_blank" href="(.*?)"',req.text,re.S)
                        for url in url_list:
                            company_url_file.write(first_cate+','+second_cate+','+url+'\n')
                            company_url_file.flush()
                            print(url)

                except Exception as e:
                    error_file.write(first_cate+','+second_cate+','+cate_url+','+page_num)
                    error_file.flush()
                    print(e,cate_url)


# 获取所有公司详情页url
def company_url_handle():
    global lock,error_file,company_url_file
    lock = Lock()
    error_file = open('error_file1.csv','w')
    company_url_file = open('company_info_url.csv','w')
    info_tuple_list = []
    with open('error_file.csv','r') as cate_url_list_file:
        for cate_url_list in cate_url_list_file.readlines():
            first_cate,second_cate,cate_url = cate_url_list.split(',')
            info_tuple_list.append((first_cate,second_cate,cate_url.strip()))

    pool = Pool(20)
    pool.map(get_company_info_url_info,info_tuple_list)
    pool.close()
    pool.join()
    error_file.close()
    company_url_file.close()

# 获取所有公司详情页url
def get_company_info_url_info(info_tuple_list):
    first_cate,second_cate,cate_url = info_tuple_list[0],info_tuple_list[1],info_tuple_list[2]
    try:
        req = requests.get(cate_url,headers=get_headers(),proxies=get_proxies_ip(),timeout=50)
        soup = BeautifulSoup(req.text,'html.parser')
        url_list = soup.select('#navindex > li.index1.b > a')[0]['href']
        lock.acquire()
        company_url_file.write(first_cate+','+second_cate+','+url_list+'\n')
        company_url_file.flush()
        lock.release()
        print(url_list)
    except Exception as e:
        lock.acquire()
        error_file.write(first_cate+','+second_cate+','+cate_url+'\n')
        error_file.flush()
        lock.release()
        print(e,cate_url)

# 获取公司内容的handle
def company_info_handle():
    global lock,error_file
    lock = Lock()
    error_file = open('error_file1.csv','w')
    info_tuple_list = []
    with open('error_file.csv','r') as cate_url_list_file:
        # dict_list = [i['company'] for i in eval(cate_url_list_file.read())['data']]
        for cate_url_list in cate_url_list_file.readlines():
            cate_url,company_name = cate_url_list.split(',')
            info_tuple_list.append((cate_url,company_name.strip()))
        #     first_cate,second_cate,cate_url = cate_url_list.split(',')
        #     info_tuple_list.append((first_cate,second_cate,cate_url.strip()))
    # print(info_tuple_list)
    pool = Pool(20)
    pool.map(get_company_info,info_tuple_list)
    pool.close()
    pool.join()
    error_file.close()

def get_company_info(info_tuple_list):
    db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    cursor=db.cursor()
    # cate_url = 'http://www.china-10.com/search/?f=&q={}'.format(info_tuple_list)
    # print(cate_url)
    first_cate = 'Top10'
    second_cate = 'Top10'
    cate_url,company_name = info_tuple_list
    try:
        time.sleep(0.8)
        req = requests.get(cate_url,headers=get_headers(),proxies=get_proxies_ip(),timeout=20)
        time.sleep(0.8)
        soup = BeautifulSoup(req.text,'html.parser')
        product = soup.select('#rightlay > div.container > div > div.block.font16 > div > span')[0].text.strip()
        # print(product)
        product_info = soup.select('#rightlay > div.container > div > div.introduce.font14 > div.desc')[0].text.replace('\n','').strip().replace("'"," ")
        # print(product_info)
        # 全1
        company_info_basic = ' '.join(i.text for i in soup.select('#infobox > div > div.swiper-container > div > div.swiper-slide > ul li'))
        # 缺2
        # company_info_basic = ' '.join(i.text for i in soup.select('#rightlay > div.container > ul li'))
        # print(company_info_basic)
        try:
            build_time = re.findall('创立时间：(.*?) ',company_info_basic,re.S)[0]
        except:
            build_time = ''
        # print(build_time)
        try:
            build_area = re.findall('发源地：(.*?) ',company_info_basic,re.S)[0]
        except:
            build_area = ''
        # print(build_area)
        try:
            leader_people = re.findall('董事长：(.*?) ',company_info_basic,re.S)[0]
        except:
            leader_people = ''
        # print(leader_people)
        try:
            server_tel = re.findall('电话：(.*?) ',company_info_basic,re.S)[0]
        except:
            server_tel = ''
        # print(server_tel)
        try:
            company_web = re.findall('url=(.*?)"',company_info_basic,re.S)[0].replace('%3A%2F%2F','://').replace('%2F','').strip('\\')
        except:
            company_web = ''
        # print(company_web)
        try:
            Top10 = re.findall('（(.*?)）',company_info_basic,re.S)[0].replace('\n','').strip()
        except:
            Top10 = ''
        # print(Top10)
        # 全1
        company_basic_baisc = ' '.join(i.text.replace(' ','_')+' ' for i in soup.select(' div.swiper-slide > div.companyinfo.font14 > div.info > ul > li'))
        # 缺2
        # company_basic_baisc = ' '.join(i.text.replace(' ','_') for i in soup.select('#companyinfo > ul > li'))
        # print(company_basic_baisc)
        # 全1
        # try:
        #     company_name = soup.select('div.swiper-slide > div.companyinfo.font14 > div.info > ul > li.name')[0].text.strip()
        # # 缺2
        # except:
        #     company_name = product_info.split('，')[0]
        # company_name = info_tuple_list
        # print(company_name)
        try:
            contact_tel = re.findall('电话：(.*?) ',company_basic_baisc,re.S)[0]
        except:
            contact_tel = ''
        # print(contact_tel)
        try:
            address = re.findall('地址：(.*?) ',company_basic_baisc,re.S)[0]
        except:
            address = ''
        # print(address)
        # 全1
        company_more_basic = ' '.join(i.text for i in soup.select('div.swiper-slide > div.companyother > ul'))
        # print(company_more_basic)
        # print(company_basic_baisc)
        try:
            famous_people = re.findall('名人：(.*?)\n',company_more_basic,re.S)[0].strip()
        except:
            famous_people = ''
        try:
            register_money = re.findall('注册资本：(.*?)\n',company_more_basic,re.S)[0].strip()
        except:
            register_money = ''
        # try:
        #     # 合1
        #     famous_people = re.findall('名人：(.*?)\n',company_basic_baisc,re.S)
        #     # famous_people = re.findall('名人：(.*?) ',company_basic_baisc,re.S)
        #     # 缺2
        # except:
        #     famous_people = ''
        # # print(famous_people)
        # try:
        #     # 合1
        #     register_money = re.findall('资本：(.*?)\n',company_basic_baisc,re.S)[0].strip()
        #     # register_money = re.findall('资本：(.*?) ',company_basic_baisc,re.S)[0].strip()
        # except:
        #     register_money = ''
        # print(register_money)
        try:
            produt_pic = ' '.join(i['src'] for i in soup.select('#marqueen2 > div > div.mar1 > div > div.img > img'))
            if 'javascript' in produt_pic:
                produt_pic = ''
        except:
            produt_pic = ''

        # print(produt_pic)
        try:
            news_url = soup.select('div.loadblockmore.font16 > a')[-3]['href']
            if 'javascript' in news_url:
                news_url = ''
        except:
            news_url = ''
        # print(news_url)
        try:
            server_url = soup.select('div.loadblockmore.font16 > a')[-2]['href']
            if 'javascript' in server_url:
                server_url = ''
        except:
            server_url = ''
        # print(server_url)
        try:
            product_url = soup.select('div.loadblockmore.font16 > a')[-1]['href']
            if 'javascript' in product_url:
                product_url = ''
        except:
            product_url = ''
        # print(famous_people)
        # print(company_name)
        # print(product,product_info,build_time,build_area,leader_people,server_tel,company_web,Top10 ,company_name ,contact_tel ,address ,famous_people,register_money ,produt_pic,news_url ,server_url ,product_url)
        try:
            insert_sql = "INSERT INTO `China10_Company_Top10`(first_cate,second_cate,product,product_info,build_time,build_area,leader_people,server_tel,company_web,Top10 ,company_name ,contact_tel ,address ,famous_people,register_money ,produt_pic,news_url ,server_url ,product_url) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(first_cate,second_cate,product,product_info,build_time,build_area,leader_people,server_tel,company_web,Top10 ,company_name ,contact_tel ,address ,famous_people,register_money ,produt_pic,news_url ,server_url ,product_url)
            cursor.execute(insert_sql)
            db.commit()
            print(company_name,' -insert')
        except Exception as e:
            db.rollback()
            # print('db-',cate_url,e)
            lock.acquire()
            error_file.write(cate_url+','+company_name+'\n')
            error_file.flush()
            lock.release()
    except Exception as e:
        lock.acquire()
        error_file.write(cate_url+','+company_name+'\n')
        error_file.flush()
        lock.release()
        # print(e,info_tuple_list)
    cursor.close()
    db.close()

# 获取新闻、产品、网点的信息
def news_shop_product_handle():
    global lock,error_file
    lock = Lock()
    error_file = open('error_file.csv','w')
    file = open('news_product_shop.csv','r')
    company_list = []
    for ff in file.readlines():
        try:
            first_cate,second_cate,company_name,shop_url,product_url = ff.split(',')
            if shop_url != '':
                if 'shop' in shop_url and 'webshop' not in shop_url:
                    need_id = shop_url.split('_')[-1].split('.')[0]
                    company_list.append((first_cate,second_cate,company_name,need_id))
                    # print(need_id)
                elif 'news' in shop_url or 'product' in shop_url:
                    need_id = shop_url.split('_')[-1].split('.')[0]
                    company_list.append((first_cate,second_cate,company_name,need_id))
                    # print(need_id)
                else:
                    pass
                    # print('sdfghjkl',shop_url)
            else:
                if 'product' in product_url or 'news' in product_url:
                    need_id = product_url.split('_')[-1].split('.')[0]
                    company_list.append((first_cate,second_cate,company_name,need_id))
                    # print(need_id)
                    # print(product_url)
                elif 'shop' in product_url and 'webshop' not in product_url:
                    need_id = product_url.split('_')[-1].split('.')[0]
                    company_list.append((first_cate,second_cate,company_name,need_id))
                    # print(need_id)
                    # print(product_url)
                else:
                    pass
                    # print('sdfghjkl',product_url)
        except:
            pass
    # print(company_list)
    pool = Pool(20)
    pool.map(get_shop_info,company_list)
    pool.close()
    pool.join()
    error_file.close()
    # print(first_cate,second_cate,company_name,shop_url,product_url)

def get_shop_info(company_list):
    db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    cursor=db.cursor()
    beiyong = []
    first_cate = company_list[0]
    second_cate = company_list[1]
    company_name = company_list[2]
    url_id = company_list[3]
    # print(first_cate,second_cate,company_name,url_id)
    # # '网点'
    # shop_url = 'http://www.china-10.com/ajaxstream/?do=loadblock&dataType=text&param=v2_shop_col1_brandid%3A{}_num%3A10_page%3A1'.format(url_id)
    # # '新闻'
    # news_url = 'http://www.china-10.com/ajaxstream/?do=loadblock&dataType=text&param=v2_news_col1_brandid%3A{}_num%3A10_page%3A1'.format(url_id)
    # '产品'
    product_url = 'http://www.china-10.com/ajaxstream/?do=loadblock&dataType=text&param=v2_product_col1_brandid%3A{}_num%3A10_page%3A1'.format(url_id)
    #
    try:
        req = requests.get(product_url,headers=get_headers(),proxies=get_proxies_ip(),timeout=50)
        info_info = req.text
        soup = BeautifulSoup(info_info,'html.parser')
        try:
            page_num = int(int(re.findall('约(.*?)条',soup.select('div.loadblockmore.font16 > a')[0].text,re.S)[0])/9)+1
        except:
            page_num = 0
        shop_info = []
        if page_num == 0:
            # 网点
            '''
            shop_name = soup.select('div > ul > li.title')
            shop_phone = re.findall('<span class="Telephone">(.*?)</span>(.*?)',info_info,re.S)
            shop_address = re.findall('<span class="Address" title="(.*?)">',info_info,re.S)
            for i in range(len(shop_name)):
                shop_info.append({'Outlets_name':shop_name[i].text,'Outlets_phone':shop_phone[i][0].strip(),'Outlets_address':shop_address[i]})
            '''
            # 新闻
            '''
            news_title = soup.select('div ul > li.title > a')
            news_info = soup.select('div > ul > li.desc')
            # '<li class="desc">(.*?)</li>'
            news_img = soup.select('div > a > img')
            # '<img src="(.*?)>'
            for i in range(len(news_title)):
                try:
                    news_imgs = news_img[i]['src']
                except:
                    news_imgs = ''
                shop_info.append({'News_title':news_title[i].text,'News_info':news_info[i].text,'News_imgs':news_imgs})
            '''
            # 产品
            product_name = soup.select('ul > li.title > span > a')
            product_price = re.findall('<span class="price font16">(.*?)</span>',info_info,re.S)
            product_img = re.findall('<img src="(.*?)"/>',info_info,re.S)
            # print(product_name,product_price,product_img)
            for i in range(len(product_name)):
                try:
                    product_imgs = product_img[i]
                except:
                    product_imgs = ''
                shop_info.append({'Product_Name':product_name[i].text,'Product_Price':product_price[i],'Product_imgs':product_imgs})
        else:
            for i in get_shop_info2((first_cate,second_cate,company_name,url_id,page_num)):
                shop_info.append(i)
        try:
            # insert_sql = "INSERT INTO `China10_Outlets`(first_cate,second_cate,company_name,Outlets) VALUES ('{}','{}','{}','{}');".format(first_cate,second_cate,company_name,json.dumps(shop_info,ensure_ascii=False))
            # insert_sql = "INSERT INTO `China10_News`(first_cate,second_cate,company_name,news) VALUES ('{}','{}','{}','{}');".format(first_cate,second_cate,company_name,json.dumps(shop_info,ensure_ascii=False))
            insert_sql = "INSERT INTO `China10_Product`(first_cate,second_cate,company_name,product) VALUES ('{}','{}','{}','{}');".format(first_cate,second_cate,company_name,json.dumps(shop_info,ensure_ascii=False))

            cursor.execute(insert_sql)
            db.commit()
            print('-insert')
        except Exception as e:
            db.rollback()
            print('db-',e)

    except:
        lock.acquire()
        error_file.write(first_cate+','+second_cate+','+company_name+'，'+url_id+'\n')
        error_file.flush()
        lock.release()
    cursor.close()
    db.close()

def get_shop_info2(beiyong):
    first_cate = beiyong[0]
    second_cate = beiyong[1]
    company_name = beiyong[2]
    url_id = beiyong[3]
    page_num = beiyong[4]


    for i in range(2,page_num+1):
        shop_url = 'http://www.china-10.com/ajaxstream/?do=loadblock&dataType=text&param=v2_shop_col1_brandid%3A{}_num%3A10_page%3A{}'.format(url_id,i)
        try:
            req = requests.get(shop_url,headers=get_headers(),proxies=get_proxies_ip(),timeout=50)
            info_info = req.text
            soup = BeautifulSoup(info_info,'html.parser')
            shop_info = []

            # 网点
            '''
            shop_name = soup.select('div > ul > li.title')
            shop_phone = re.findall('<span class="Telephone">(.*?)</span>(.*?)',info_info,re.S)
            shop_address = re.findall('<span class="Address" title="(.*?)">',info_info,re.S)
            for i in range(len(shop_name)):
                shop_info.append({'Outlets_name':shop_name[i].text,'Outlets_phone':shop_phone[i][0].strip(),'Outlets_address':shop_address[i]})
            '''
            # 新闻
            '''
            news_title = soup.select('div ul > li.title > a')
            news_info = soup.select('div > ul > li.desc')
            news_img = soup.select('div > a > img')
            for i in range(len(news_title)):
                try:
                    news_imgs = news_img[i]['src']
                except:
                    news_imgs = ''
                shop_info.append({'News_title':news_title[i].text,'News_info':news_info[i].text,'News_imgs':news_imgs})
            '''
            # 产品
            product_name = soup.select('ul > li.title > span > a')
            product_price = re.findall('<span class="price font16">(.*?)</span>',info_info,re.S)
            product_img = re.findall('<img src="(.*?)"/>',info_info,re.S)
            # print(product_name,product_price,product_img)
            for i in range(len(product_name)):
                try:
                    product_imgs = product_img[i]
                except:
                    product_imgs = ''
                shop_info.append({'Product_Name':product_name[i].text,'Product_Price':product_price[i],'Product_imgs':product_imgs})

            return shop_info

            # try:
            #     insert_sql = "INSERT INTO `China10_Outlets`(first_cate,second_cate,company_name,Outlets) VALUES ('{}','{}','{}','{}');".format(first_cate,second_cate,company_name,json.dumps(shop_info,ensure_ascii=False))
            #     cursor.execute(insert_sql)
            #     db.commit()
            #     print('-insert')
            # except Exception as e:
            #     db.rollback()
            #     print('db-',e)
        except:
            lock.acquire()
            error_file.write(first_cate+','+second_cate+','+company_name+'，'+url_id+'\n')
            error_file.flush()
            lock.release()



def text():
    first_cate = 'Top10'
    second_cate = 'Top10'
    db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    cursor=db.cursor()
    with open('text.html','r') as text_file:
        info_info = text_file.read()
        soup = BeautifulSoup(info_info,'html.parser')

        product = soup.select('#rightlay > div.container > div > div.block.font16 > div > span')[0].text.strip()
        # print(product)
        product_info = soup.select('#rightlay > div.container > div > div.introduce.font14 > div.desc')[0].text.replace('\n','').strip().replace("'"," ")
        # print(product_info)
        # 全1
        company_info_basic = ' '.join(i.text for i in soup.select('#infobox > div > div.swiper-container > div > div.swiper-slide > ul li'))
        # 缺2
        # company_info_basic = ' '.join(i.text for i in soup.select('#rightlay > div.container > ul li'))
        # print(company_info_basic)
        try:
            build_time = re.findall('创立时间：(.*?) ',company_info_basic,re.S)[0]
        except:
            build_time = ''
        # print(build_time)
        try:
            build_area = re.findall('发源地：(.*?) ',company_info_basic,re.S)[0]
        except:
            build_area = ''
        # print(build_area)
        try:
            leader_people = re.findall('董事长：(.*?) ',company_info_basic,re.S)[0]
        except:
            leader_people = ''
        # print(leader_people)
        try:
            server_tel = re.findall('电话：(.*?) ',company_info_basic,re.S)[0]
        except:
            server_tel = ''
        # print(server_tel)
        try:
            company_web = re.findall('url=(.*?)"',company_info_basic,re.S)[0].replace('%3A%2F%2F','://').replace('%2F','').strip('\\')
        except:
            company_web = ''
        # print(company_web)
        try:
            Top10 = re.findall('（(.*?)）',company_info_basic,re.S)[0].replace('\n','').strip()
        except:
            Top10 = ''
        # print(Top10)
        # 全1
        company_basic_baisc = ' '.join(i.text.replace(' ','_')+' ' for i in soup.select(' div.swiper-slide > div.companyinfo.font14 > div.info > ul > li'))
        # 缺2
        # company_basic_baisc = ' '.join(i.text.replace(' ','_') for i in soup.select('#companyinfo > ul > li'))
        # print(company_basic_baisc)
        # 全1
        # try:
        #     company_name = soup.select('div.swiper-slide > div.companyinfo.font14 > div.info > ul > li.name')[0].text.strip()
        # # 缺2
        # except:
        #     company_name = product_info.split('，')[0]
        company_name = '摩恩(上海)厨卫有限公司'
        # print(company_name)
        try:
            contact_tel = re.findall('电话：(.*?) ',company_basic_baisc,re.S)[0]
        except:
            contact_tel = ''
        # print(contact_tel)
        try:
            address = re.findall('地址：(.*?) ',company_basic_baisc,re.S)[0]
        except:
            address = ''
        # print(address)
        # 全1
        company_more_basic = ' '.join(i.text for i in soup.select('div.swiper-slide > div.companyother > ul'))
        # print(company_more_basic)
        # print(company_basic_baisc)
        try:
            famous_people = re.findall('名人：(.*?)\n',company_more_basic,re.S)[0].strip()
        except:
            famous_people = ''
        try:
            register_money = re.findall('注册资本：(.*?)\n',company_more_basic,re.S)[0].strip()
        except:
            register_money = ''
        # try:
        #     # 合1
        #     famous_people = re.findall('名人：(.*?)\n',company_basic_baisc,re.S)
        #     # famous_people = re.findall('名人：(.*?) ',company_basic_baisc,re.S)
        #     # 缺2
        # except:
        #     famous_people = ''
        # # print(famous_people)
        # try:
        #     # 合1
        #     register_money = re.findall('资本：(.*?)\n',company_basic_baisc,re.S)[0].strip()
        #     # register_money = re.findall('资本：(.*?) ',company_basic_baisc,re.S)[0].strip()
        # except:
        #     register_money = ''
        # print(register_money)
        try:
            produt_pic = ' '.join(i['src'] for i in soup.select('#marqueen2 > div > div.mar1 > div > div.img > img'))
            if 'javascript' in produt_pic:
                produt_pic = ''
        except:
            produt_pic = ''

        # print(produt_pic)
        try:
            news_url = soup.select('div.loadblockmore.font16 > a')[-3]['href']
            if 'javascript' in news_url:
                news_url = ''
        except:
            news_url = ''
        # print(news_url)
        try:
            server_url = soup.select('div.loadblockmore.font16 > a')[-2]['href']
            if 'javascript' in server_url:
                server_url = ''
        except:
            server_url = ''
        # print(server_url)
        try:
            product_url = soup.select('div.loadblockmore.font16 > a')[-1]['href']
            if 'javascript' in product_url:
                product_url = ''
        except:
            product_url = ''
        # print(famous_people)
        # print(company_name)
        # print(product,product_info,build_time,build_area,leader_people,server_tel,company_web,Top10 ,company_name ,contact_tel ,address ,famous_people,register_money ,produt_pic,news_url ,server_url ,product_url)
        try:
            insert_sql = "INSERT INTO `China10_Company_Top10`(first_cate,second_cate,product,product_info,build_time,build_area,leader_people,server_tel,company_web,Top10 ,company_name ,contact_tel ,address ,famous_people,register_money ,produt_pic,news_url ,server_url ,product_url) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(first_cate,second_cate,product,product_info,build_time,build_area,leader_people,server_tel,company_web,Top10 ,company_name ,contact_tel ,address ,famous_people,register_money ,produt_pic,news_url ,server_url ,product_url)
            cursor.execute(insert_sql)
            db.commit()
            print(company_name,' -insert')
        except Exception as e:
            db.rollback()
            # print('db-',cate_url,e)


text()
