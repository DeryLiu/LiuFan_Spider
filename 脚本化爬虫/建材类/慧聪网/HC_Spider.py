'http://market.hc360.com/bm/'
from bs4 import BeautifulSoup
import time,pymysql
from multiprocessing import Pool,Lock
from selenium import webdriver
import requests,re,random,json
import http.cookiejar

'''
# phontomjs 设置代理
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0")
dcap["phantomjs.page.settings.resourceTimeout"] = ("1000")
service_args = [
    '--proxy=127.0.0.1:1080'
    ] #默认为http代理，可以指定proxy type
newdriver = webdriver.PhantomJS(service_args=service_args, desired_capabilities=dcap)

# 法二
# 不使用代理代打开ip138
browser=webdriver.PhantomJS(PATH_PHANTOMJS)
browser.get('http://1212.ip138.com/ic.asp')
print('1: ',browser.session_id)
print('2: ',browser.page_source)
print('3: ',browser.get_cookies())

# 利用DesiredCapabilities(代理设置)参数值，重新打开一个sessionId，我看意思就相当于浏览器清空缓存后，加上代理重新访问一次url
proxy=webdriver.Proxy()
proxy.proxy_type=ProxyType.MANUAL
proxy.http_proxy='1.9.171.51:800'
# 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中
proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
browser.get('http://1212.ip138.com/ic.asp')
print('1: ',browser.session_id)
print('2: ',browser.page_source)
print('3: ',browser.get_cookies())

# 还原为系统代理
proxy=webdriver.Proxy()
proxy.proxy_type=ProxyType.DIRECT
proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
browser.get('http://1212.ip138.com/ic.asp')

# --
# chrome driver 设置代理

PROXY_IP = "<some IP address>"

options = webdriver.ChromeOptions()
options.add_argument("--proxy-server=%s" % (UID,PWD,PROXY_IP))

driver = webdriver.Chrome(executable_path=".\\driver\\chromedriver.exe",
                          chrome_options=options)
driver.get("<site URL>")
'''

class HC_Spider():
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
    def get_headers(self):
        headers = {
            'User-Agent':random.choice(self.USER_AGENTS),
        }
        return headers

    def get_proxies_ip(self):
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
        return random.choice(proxies_list)
        # return proxies

    # 根据分类找到所有产品的url
    def get_product_info_by_phontomJS(self):
        # driver = webdriver.Chrome(executable_path='/Users/Dery/SeleniumWebDriver/chromedriver')
        PROXY_IP = self.get_proxies_ip()
        print(PROXY_IP)
        options = webdriver.ChromeOptions()
        options.add_argument("--proxy-server={}".format(PROXY_IP))
        driver = webdriver.Chrome(executable_path='/Users/Dery/SeleniumWebDriver/chromedriver',chrome_options=options)
        # driver.save_screenshot('./data/login_picture1.png')

        # phantomJS
        all_category_info_all = open('all_cate_url.csv','r')
        error_file = open('error_file.csv','w')
        time_sleep = [5,6,7,8,9,10,11]
        with open('all_company_url.csv','w') as all_company_url_file:
            for all_category in all_category_info_all.readlines():
                first_name,second_name,cate_url,page_num = all_category.split(',')
                # print(first_name,second_name,cate_url,page_num)
                url_list = [cate_url.format(i) for i in range(1,int(page_num.strip())+1)]
                #-------------------
                for url in url_list:
                    try:
                        time.sleep(random.choice(time_sleep))
                        # print(campany_url)
                        driver.get(url)
                        js10=["document.body.scrollTop={}".format(1200*i) for i in range(7)]
                        # 'document.body.scrollWidth'
                        # print(js10)
                        for js in js10:
                            time.sleep(1)
                            driver.execute_script(js)
                        time.sleep(0.5)
                        # print(driver.page_source)
                        soup = BeautifulSoup(driver.page_source,'html.parser')
                        company_url_list = soup.select('div.picmid.pRel > a')
                        for ti in company_url_list:
                            all_company_url_file.write(first_name+','+second_name+','+ti['href']+'\n')
                            all_company_url_file.flush()
                            print(ti['href'])

                    except Exception as e:
                        error_file.write(first_name+','+second_name+','+cate_url+'\n')
                        error_file.flush()
                        print(e)
        driver.quit()

    # 获取所有的公司地址 phantomjs
    def get_company_info_by_phontomJS(self):
        # driver = webdriver.Chrome(executable_path='/Users/Dery/SeleniumWebDriver/chromedriver')
        PROXY_IP = self.get_proxies_ip()
        print(PROXY_IP)
        options = webdriver.ChromeOptions()
        options.add_argument("--proxy-server={}".format(PROXY_IP))
        driver = webdriver.Chrome(executable_path='/Users/Dery/SeleniumWebDriver/chromedriver',chrome_options=options)
        # driver.save_screenshot('./data/login_picture1.png')
        # phantomJS
        all_category_info_all = open('cate_bussiness_basic.csv','r')
        error_file = open('error_file.csv','w')
        time_sleep = [2]
        with open('all_company_url.csv','w') as all_company_url_file:
            for all_category in all_category_info_all.readlines():
                first_name,second_name,cate_url,page_num = all_category.split(',')
                # print(first_name,second_name,cate_url,page_num)
                if page_num.strip() == '1':
                    url_list = [cate_url]
                else:
                    url_list = [cate_url.format(i) for i in range(1,int(page_num.strip())+1)]
                #--------------------
                for url in url_list:
                    try:
                        time.sleep(random.choice(time_sleep))
                        # print(campany_url)
                        driver.get(url)
                        js10=["document.body.scrollTop={}".format(1200*i) for i in range(7)]
                        # 'document.body.scrollWidth'
                        # print(js10)
                        for js in js10:
                            time.sleep(1)
                            driver.execute_script(js)
                        time.sleep(0.5)
                        # print(driver.page_source)
                        soup = BeautifulSoup(driver.page_source,'html.parser')

                        company_url = soup.select('ul > li > div > div.seaNewList > dl > dd.newCname > p > a')
                        for com_info in company_url:
                            all_company_url_file.write(first_name+','+second_name+','+com_info['href']+'/shop/show.html'+','+com_info['title']+'\n')
                            all_company_url_file.flush()
                            print(com_info['title'])

                    except Exception as e:
                        error_file.write(first_name+','+second_name+','+cate_url+'\n')
                        error_file.flush()
                        print(e)
        driver.quit()

    # 获取产品信息
    def get_product_info(self):
        db = pymysql.connect("localhost","root","xxx","xxx",charset='utf8')
        cursor=db.cursor()

        # chrome driver
        PROXY_IP = self.get_proxies_ip()
        options = webdriver.ChromeOptions()
        options.add_argument("--proxy-server={}".format(PROXY_IP))
        # 不加载图片
        # prefs = {"profile.managed_default_content_settings.images":2}
        # options.add_experimental_option("prefs",prefs)

        driver = webdriver.Chrome(executable_path='/Users/Dery/SeleniumWebDriver/chromedriver',chrome_options=options)

        # # phontomJS
        # dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)
        # dcap["phantomjs.page.settings.userAgent"] = (random.choice(self.USER_AGENTS))
        # dcap["phantomjs.page.settings.resourceTimeout"] = ("1000")
        # service_args = ['--proxy={}'.format(self.get_proxies_ip())] #默认为http代理，可以指定proxy type
        # driver = webdriver.PhantomJS(executable_path='/Users/Dery/SeleniumWebDriver/phantomjs-2.1.1-macosx/bin/phantomjs',service_args=service_args, desired_capabilities=dcap)

        all_company_url_file = open('company_url.csv','r')
        for company_url_file in all_company_url_file.readlines():
            first_cate,second_cate,company_url = company_url_file.split(',')
            try:
                driver.get(company_url.strip())
                soup = BeautifulSoup(driver.page_source,'html.parser')

                # 公司名
                try:
                    company_name = soup.select('div.main-detail-info > div.main-sidbar-left > div.mmt-years > div.comply-name > p > a')[0].text
                except:
                    company_name = soup.select('#comTitle')[0].text
                # 产品图片
                img_info = []
                img_info.append(soup.select('#imgContainer > div.zoomPad > img')[0]['src'])
                img_list = soup.select('#thumblist > li > div > a > img')
                for img in img_list:
                    img_url = img['src'].replace('100x100','600x600')
                    img_info.append(img_url)
                # 产品名
                product_name = soup.select('#comTitle')[0].text
                # 价格
                try:
                    price = soup.select('#oriPriceTop')[0].text.replace('¥','').replace('?','').strip()
                except:
                    price = soup.select('body > div.content.w1190 > div.syDetailTop > div.product-box > div.detail-right-con > div.item-row-w.promot-price > span.item-price-r')[0].text.strip()
                # 基本参数
                # slesimu = soup.select('#pdetail > div.d-vopy > table')[0].text.strip()
                slesimu = soup.select('#pdetail > div.d-vopy > table')[0].text.replace('\n','').replace('	','').replace('                            ','').strip()
                # 品牌
                try:
                    product = slesimu.split('品牌：')[1].split(' ')[0]
                except:
                    product = ''
                # 详细说明
                intruction = soup.select('#introduce')[0].text.replace('..','').strip()

                try:
                    # search_sql = "SELECT * FROM `HuiCong` WHERE concat(product_name,company_name) LIKE '{}' AND concat(product_name,company_name) LIKE '{}';".format(product_name,company_name)
                    # cursor.execute(search_sql)
                    # if len(cursor.fetchall()):
                    #     update_sql = "UPDATE HuiCong SET first_cate='{}',second_cate='{}',company_name='{}',product='{}',img='{}',product_name='{}',price='{}',slesimu='{}',intructon='{}'".format(first_cate,second_cate,company_name,product,','.join(list(set(img_info))),product_name,price,slesimu,intruction)+" WHERE concat(product_name,company_name) LIKE '{}' AND concat(product_name,company_name) LIKE '{}';".format(product_name,company_name)
                    #     # print(update_sql)
                    #     cursor.execute(update_sql)
                    #     db.commit()
                    #     print(product,' -update')
                    # else:
                    insert_sql = "INSERT INTO `HuiCong`(first_cate,second_cate,company_name,product,img,product_name,price,slesimu,intructon) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(first_cate,second_cate,company_name,product,','.join(list(set(img_info))),product_name,price,slesimu,intruction)
                    cursor.execute(insert_sql)
                    db.commit()
                    print(product,' -insert')

                except Exception as e:
                    db.rollback()
                    print('db-',e)

            except Exception as e:
                db.rollback()
                print(e)

# 20170512 - 二次改版
# 获取所有公司的url
def save_company_name_handle():
    global lock,error_file,company_url_file
    error_file = open('error.csv','w')
    company_url_file = open('company_url_new.csv','w')
    info_list = []
    with open('all_cate_url.csv','r') as all_cate_url_file:
        for all_cate_url in all_cate_url_file.readlines():
            first_cate,second_cate,cate_url,page_num = all_cate_url.split(',')
            for i in range(1,int(page_num)+1):
                page1 = cate_url.format(i)+'&ap=A&t=1&af=0&afadprenum=0&afadbeg={}'.format(21+(i-1)*60)
                page2 = cate_url.format(i)+'&ap=A&t=1&af=1&afadprenum=0&afadbeg={}'.format(21+(i-1)*60)
                page3 = cate_url.format(i)+'&ap=A&t=1&af=2&afadprenum=0&afadbeg={}'.format(21+(i-1)*60+20)
                info_list.append((first_cate,second_cate,page1))
                info_list.append((first_cate,second_cate,page2))
                info_list.append((first_cate,second_cate,page3))
    pool = Pool(20)
    pool.map(save_company_name,info_list)
    pool.close()
    pool.join()
    error_file.close()
    company_url_file.close()

def save_company_name(info_list):
    first_cate,second_cate,page_url = info_list[0:3]
    try:
        response = requests.get(page_url,headers=hc.get_headers(),proxies=hc.get_proxies_ip(),timeout=60)
        soup = BeautifulSoup(response.text,'html.parser')
        company_url = soup.select('dd.newCname > p > a')
        for i in company_url:
            try:
                company_u = i['href']+'/shop/show.html'
                company_t = i['title']
                # print(i['href']+'/shop/show.html',i['title'])
                lock.acquire()
                company_url_file.write(first_cate+','+second_cate+','+company_u+','+company_t+'\n')
                company_url_file.flush()
                lock.release()
                print(company_t)
            except:
                pass

    except Exception as e:
        lock.acquire()
        error_file.write(first_cate+','+second_cate+','+page_url+'\n')
        error_file.flush()
        lock.release()
        print(e)


# 获取公司信息
def handle():
    global lock,error_file
    lock = Lock()
    error_file = open('error.csv','w')
    info_tuple_list = []
    with open("companyURL_title.csv","r") as companyURL_title_file:
        for companyURL_title in companyURL_title_file.readlines():
            first_cate,second_cate,company_url,company_name = companyURL_title.split(",")
            info_tuple_list.append((first_cate,second_cate,company_url,company_name.strip()))

    pool = Pool(20)
    pool.map(get_info,info_tuple_list)
    pool.close()
    pool.join()
    error_file.close()
# 获取公司信息
def get_info(info_tuple_list):
# def get_info(cate,basic_url):
    db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    cursor=db.cursor()

    first_cate = info_tuple_list[0]
    second_cate = info_tuple_list[1]
    company_url = info_tuple_list[2]
    company_name = info_tuple_list[3]

    try:
        req = requests.get(company_url,headers=hc.get_headers(),proxies=hc.get_proxies_ip(),timeout=50)
        req.encoding = 'gb2312'
        soup = BeautifulSoup(req.text,'html.parser')
        str_soup = soup.text
        # print(soup.text)
        # company_info = {'company_info':soup.select('#companyIntroduce > div.contentbox > div.txtb > div > div')[-1].text.split(';')[-1].replace('\n','').strip()}
        # company_info = {'company_info':soup.select('#companyIntroduce > div.introBox > span')[0].text.replace('\n','').strip()}
        company_info = {'company_info':soup.select('#companyIntroduce > div.introBox > div > span')[0].text.replace('\n','').strip()}
        # company_info = {'company_info':soup.select('body > div.content.w1190 > div.c-left.fl > div:nth-child(4) > div.company-words > p')[-1].text.split(';')[-1].replace('\n','').strip()}
        # company_info = {'company_info':soup.select('body > div.content > div.c-left.fl > div > div.company-words > p')[0].text.replace('\n','').strip()}
        # print(company_info)

        # meta_description = re.findall('<meta content="慧聪网（Hc360.Com）(.*?)欢迎联系洽谈！',str(soup.select('html meta')),re.S)[0]
        # meta_description = '慧聪'+re.findall('<meta content="慧聪(.*?)欢迎联系洽谈！',str(soup.select('html meta')),re.S)[0]
        try:
            area = re.findall('所在地区：(.*?)\n',str_soup,re.S)[0].strip()
        except:
            area = ''
        try:
            register_info = re.findall('工商注册信息：(.*?)\n',str_soup,re.S)[0].strip()
        except:
            register_info = ''
        try:
            Specialized_services = re.findall('主营产品或服务:(.*?)主营行业',str_soup,re.S)[0].replace('\n','').replace('	','').strip()
        except:
            Specialized_services = ''
        try:
            major = re.findall('主营行业:(.*?)企业类型',str_soup,re.S)[0].strip()
        except:
            major = re.findall('主营行业:(.*?)主营产品',str_soup,re.S)[0].strip()
        # print(major)
        try:
            company_type = re.findall('企业类型：(.*?)经营模式：',str_soup,re.S)[0].strip()
        except:
            company_type = ''
        # print(company_type)
        try:
            business_model = re.findall('经营模式：(.*?)注册地址：',str_soup,re.S)[0].strip()
        except:
            business_model = ''
        # print(business_model)
        try:
            registered_address = re.findall('注册地址：(.*?)经营地址：',str_soup,re.S)[0].strip()
        except:
            registered_address = ''
        # print(registered_address)
        try:
            business_address = re.findall('经营地址：(.*?)公司成立时间：',str_soup,re.S)[0].strip()
        except:
            business_address = re.findall('经营地址：(.*?)注册时间：',str_soup,re.S)[0].strip()
        # print(business_address)
        try:
            establishing_time= re.findall('公司成立时间：(.*?)法定代表人',str_soup,re.S)[0].strip()
        except:
            establishing_time = re.findall('注册时间：(.*?)注册资本',str_soup,re.S)[0].strip()
        # print(establishing_time)
        try:
            principal = re.findall('法定代表人/负责人：(.*?)员工人数',str_soup,re.S)[0].strip()
        except:
            principal = ''
        try:
            employees_nums = re.findall('员工人数：(.*?)年营业额',str_soup,re.S)[0].strip()
        except:
            employees_nums = ''
        try:
            annual_sales = re.findall('年营业额：(.*?)经营品牌',str_soup,re.S)[0].strip()
        except:
            annual_sales = ''
        try:
            product = re.findall('经营品牌：(.*?)注册资本',str_soup,re.S)[0].strip()
        except:
            product = ''
        try:
            registered_capital = re.findall('注册资本：(.*?)主要客户群',str_soup,re.S)[0].strip()
        except:
            registered_capital = ''
        try:
            major_client = re.findall('主要客户群：(.*?)主要市场',str_soup,re.S)[0].strip()
        except:
            major_client = ''
        try:
            major_market = re.findall('主要市场：(.*?)年出口额',str_soup,re.S)[0].strip()
        except:
            major_market = ''

        # print(establishing_time,principal,employees_nums,annual_sales,product,registered_capital,major_client,major_market)
        try:
            annual_export = re.findall('年出口额：(.*?)年进口额',str_soup,re.S)[0].strip()
        except:
            annual_export = ''
        # print(annual_export)
        try:
            annual_imports = re.findall('年进口额：(.*?)开户银行',str_soup,re.S)[0].strip()
        except:
            annual_imports = ''
        # print(annual_imports)
        try:
            opening_bank = re.findall('开户银行：(.*?)银行帐号',str_soup,re.S)[0].strip()
        except:
            opening_bank = ''
        # print(opening_bank)
        try:
            RD_nums = re.findall('研发部门人数：(.*?)月产量',str_soup,re.S)[0].strip()
        except:
            RD_nums = ''
        # print(RD_nums)
        try:
            monthl_output = re.findall('月产量：(.*?)吨',str_soup,re.S)[0].strip()
        except:
            monthl_output = ''
        # print(monthl_output)
        try:
            plant_area = re.findall('厂房面积：(.*?)质量控制',str_soup,re.S)[0].strip()
        except:
            plant_area = ''
        # print(plant_area)
        try:
            system_certification = re.findall('管理体系认证：(.*?)认证信息',str_soup,re.S)[0].strip()
        except:
            system_certification = ''
        # print(system_certification)
        try:
            try:
                contact_name = re.findall('联系人：(.*?)\n',str_soup,re.S)[0].strip()
            except:
                contact_name = re.findall('var contactor= "(.*?)";',str_soup,re.S)[0].strip()
        except:
            contact_name = re.findall('联系我们\n更多>>(.*?)电话',str_soup,re.S)[0].strip()
        try:
            try:
                contact_phone = re.findall('手机：(.*?)\n',str_soup,re.S)[0].strip()
            except:
                contact_phone = re.findall('手机 ：(.*?) ',str_soup,re.S)[0].strip()
        except:
            contact_phone = ''
        try:
            try:
                contact_tel = re.findall('电话：(.*?)\n',str_soup,re.S)[0].strip()
            except:
                contact_tel = re.findall('电话 ：(.*?) ',str_soup,re.S)[0].strip()
        except:
            contact_tel = ''

        # print(cate,commenter,product_name,comment_type,comments_info,comment_time)
        try:
            insert_sql = "INSERT INTO `HuiCong_Company`(first_cate,second_cate,company_name,register_info,area,Specialized_services,major,company_type,business_model,registered_address,business_address,establishing_time,principal,employees_nums,annual_sales,product,registered_capital,major_client,major_market,annual_export,annual_imports,opening_bank,R_D_nums,plant_area,system_certification,monthl_output,contact_name,contact_phone,contact_tel) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(first_cate,second_cate,company_name,register_info,area,Specialized_services,major,company_type,business_model,registered_address,business_address,establishing_time,principal,employees_nums,annual_sales,product,registered_capital,major_client,major_market,annual_export,annual_imports,opening_bank,RD_nums,plant_area,system_certification,monthl_output,contact_name,contact_phone,contact_tel)
            cursor.execute(insert_sql)
            db.commit()
            print(contact_name,' -insert')
        except Exception as e:
            db.rollback()
            print(company_url,e)

    except Exception as e:
        lock.acquire()
        error_file.write(first_cate+','+second_cate+','+company_url+','+company_name+'\n')
        error_file.flush()
        lock.release()
        print(company_url)
        print(e)

    cursor.close()
    db.close()


'''20170515 新增'''
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

def get_product_handle():
    global request_error,LinSHi,lock
    lock = Lock()

    request_error = open('request_error.csv','w')
    '分类，产品名，价格，图片，参数'
    LinSHi = open('LinShi1.csv','w')
    info_list = []

    # with open('companyURL_title.csv','r') as companyURL_title:
    with open('request_error1.csv','r') as companyURL_title:
        for company_info in companyURL_title.readlines():
            first_cate,second_cate,company_url_was,company_name = company_info.split(",")
            company_url = company_url_was.replace('show','businwindow')
            info_list.append((first_cate,second_cate,company_url,company_name))

        pool = Pool(15)
        pool.map(get_product_info,info_list)
        pool.close()
        pool.join()
        request_error.close()
        LinSHi.close()

def get_product_info(info_list):
    first_cate,second_cate,company_url,company_name = info_list[0:4]
    try:
        respnonse = requests.get(company_url,headers=get_headers(),proxies=get_proxies_ip(),timeout=60)
        respnonse.encoding = 'gb2312'
        soup = BeautifulSoup(respnonse.text,'html.parser')
        try:
            # page_num = re.findall('共(.*?)页',str(soup.select('div.ProlistCont > div.ListModMain > div.s-mod-page > span.total')),re.S)[0]
            page_num = re.findall('共(.*?)页',str(soup.select('div.ProDirectory > div.pageNew > div > div > span.pageLeft')),re.S)[0]
        except:
            page_num = '1'
            # page_num = re.findall('共(.*?)页',str(soup.select('body > div.content.w1190 > div.c-left.fl > div.goods-box.product-every > div.s-mod-page > div > span.total')),re.S)[0]
        lock.acquire()
        LinSHi.write(first_cate+','+second_cate+','+company_url+','+company_name.strip()+','+page_num+'\n')
        LinSHi.flush()
        lock.release()
        print(page_num)
    except Exception as e:
        lock.acquire()
        request_error.write(first_cate+','+second_cate+','+company_url+','+company_name)
        request_error.flush()
        lock.release()
        # print(company_url,e)

def get_product_url_handle():
    global lock,company_product_url,error_file
    company_product_url = open('company_product_url.csv','w')
    error_file = open('error_file.csv','w')
    lock = Lock()
    insert_info = []
    with open('Company_prouct_page.csv','r') as Company_prouct_page:
        for Company_prouct in Company_prouct_page.readlines():
            first_cate,second_cate,company_url,company_name,page_num_str = Company_prouct.split(',')
            insert_info = []
            if page_num_str.strip() == '1':
                insert_info.append((first_cate,second_cate,company_url,company_name))
                # print(first_cate,second_cate,company_url,company_name,page_num_str)
            else:
                for url in [company_url.replace('businwindow','businwindow-{}').format(i) for i in range(1,int(page_num_str)+1)]:
                    insert_info.append((first_cate,second_cate,url,company_name))
            # print(insert_info)

    # Company_prouct_page = open('XXXXXXXXX.csv','r')
    # for Company_prouct in Company_prouct_page.readlines():
    #     first_cate,second_cate,company_url,company_name = Company_prouct.split(',')
    #     insert_info.append((first_cate,second_cate,company_url,company_name.strip()))

    pool = Pool(10)
    pool.map(get_product_url,insert_info)
    pool.close()
    pool.join()

    company_product_url.close()
    error_file.close()

def get_product_url(insert_info):
    first_cate,second_cate,company_url,company_name = insert_info
    # print(first_cate,second_cate,company_url,company_name)
    try:
        responseLF = requests.get(company_url,headers=get_headers(),proxies=get_proxies_ip())
        soup = BeautifulSoup(responseLF.text,'html.parser')
        cate_info = {'cate_info':''.join([i.text.replace('\n','').replace('\t','').replace('全部','').replace('\r','').replace(',','').strip() for i in soup.select('#mainContList')])}
        product_info =  soup.select('div.ProlistCont > div.ListModMain > div.itemListMod > ul > li > dl > dt > a')
        price_info = soup.select('div.ProlistCont > div.ListModMain > div.itemListMod > ul > li > dl > dd.itemPrice')
        for i in range(len(product_info)):
            product_url,product_name,price = product_info[i]['href'],product_info[i]['title'],price_info[i].text
            lock.acquire()
            company_product_url.write(first_cate+','+second_cate+','+company_url+','+company_name.replace(',','')+','+json.dumps(cate_info,ensure_ascii=False)+','+product_url+','+product_name.replace(',','')+','+price+'\n')
            company_product_url.flush()
            lock.release()
            print(product_name)
    except:
        lock.acquire()
        error_file.write(first_cate+','+second_cate+','+company_url+','+company_name+'\n')
        error_file.flush()
        lock.release()
        print(company_url)

def get_product_info_handle():
    global lock,error_file,HCdb,HCcursor
    lock = Lock()
    HCdb = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    # db = pymysql.connect("192.168.1.231","root","3jw9lketj0","ConstructionMaterials",charset='utf8')
    HCcursor = HCdb.cursor()

    info_tuple = []
    company_product_url = open('company_product_url.csv','r')
    error_file = open('error_file.csv','w')
    for Company_prouct in company_product_url.readlines():
        '''卫浴洁具,淋浴水龙头,http://zjoukaidi.b2b.hc360.com/shop/businwindow-1.html,温州市龙湾海城欧凯迪洁具厂,{"cate_info": "厨房水龙头  四方水龙头  弹簧菜盘水龙头  三联瀑布浴缸系列  宽嘴瀑布水龙头系列  抽拉水龙头  单孔水龙头  玉葫芦系列  未分类"},http://b2b.hc360.com/supplyself/600401844.html,欧凯迪厂家直销全铜水龙头厨房水龙头弹簧菜盘水龙头okd9021,￥175.00元/件'''
        try:
            first_cate,second_cate,company_url,company_name,cate_info,product_url,product_name,product_prict = Company_prouct.split(',')
            info_tuple.append((first_cate,second_cate,company_url,company_name,cate_info,product_url,product_name,product_prict.strip()))
        except:
            pass
    pool = Pool(20)
    pool.map(get_product_basic_info,info_tuple)
    pool.close()
    pool.join()
    error_file.close()
    HCdb.close()
    HCcursor.close()

def get_product_basic_info(info_tuple):

    first_cate,second_cate,company_url,company_name,cate_info,product_url,product_name,product_price = info_tuple
    try:
        HC_response = requests.get(product_url,headers=get_headers(),timeout=30)
        HC_response.encoding = 'gbk'
        soup = BeautifulSoup(HC_response.text,'html.parser')
        img_list = ' '.join(i['src'].replace('100x100','600x600') for i in soup.select('#thumblist > li > div > a > img'))
        product_area = soup.select('div.item-mmt-txt > ul > li > div > p')[0].text
        basic_data = ' '.join(i.text.replace('\n','').replace('\t','').replace('  ','').replace('同参数产品',' ').strip() for i in soup.select('#pdetail > div.d-vopy > table'))

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
        error_file.write(first_cate+','+second_cate+','+company_url+','+company_name+','+cate_info+','+product_url+','+product_name+','+product_prict+'\n')
        error_file.flush()
        lock.release()

def text():
    with open("textHUICONG.html",'r',encoding='gbk') as text_fuule:
        soup = BeautifulSoup(text_fuule.read(),'html.parser')
        cate_info = ''.join([i.text.replace('\n','').replace('\t','').replace('全部','').strip() for i in soup.select('#mainContList')])

        product_info =  soup.select('div.ProlistCont > div.ListModMain > div.itemListMod > ul > li > dl > dt > a')
        price_info = soup.select('div.ProlistCont > div.ListModMain > div.itemListMod > ul > li > dl > dd.itemPrice')

        for i in range(len(product_info)):
            product_url,product_name,price = product_info[i]['href'],product_info[i]['title'],price_info[i].text
            print(product_url,product_name,price)
        # for price_i in soup.select('div.ProlistCont > div.ListModMain > div.itemListMod > ul > li > dl > dd.itemPrice'):
        #     print(price_i.text)
        print(cate_info)


if __name__ == '__main__':

    hc = HC_Spider()
    # hc.text()
    # hc.get_product_info()

    # 20170512 - 二次改版
    # 获取所有公司的url
    # save_company_name_handle()

    # 公司的产品:
    # text()
    # get_product_handle()

    # text()
    get_product_url_handle()