import requests
from bs4 import BeautifulSoup
from random import choice
import pymysql
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import random
from multiprocessing import Pool,Lock
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        'http':'http://'+choice(proxies_list)
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
    return random.choice(USER_AGENTS)
    # return {
    #     'User-Agent': choice(USER_AGENTS),
    #     # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #     # 'Accept-Language': 'en-US,en;q=0.5',
    #     # 'Connection': 'keep-alive',
    #     # 'Accept-Encoding': 'gzip, deflate',
    # }

def get_all_company_by_phantomJS(need_info_list):
    # 引入配置对象DesiredCapabilities
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # #从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
    # dcap["phantomjs.page.settings.userAgent"] = (get_headers())
    # # 不载入图片，爬页面速度会快很多
    # dcap["phantomjs.page.settings.loadImages"] = False
    # # 设置代理
    # service_args = ['--proxy=127.0.0.1:9999','--proxy-type=socks5']
    # #打开带配置信息的phantomJS浏览器
    # driver = webdriver.PhantomJS(executable_path='/Users/Dery/phantomjs-2.1.1-macosx/bin/phantomjs', desired_capabilities=dcap,service_args=service_args)
    # # 隐式等待5秒，可以自己调节
    # driver.implicitly_wait(5)
    # # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
    # # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
    # driver.set_page_load_timeout(10)
    # # 设置10秒脚本超时时间
    # driver.set_script_timeout(10)
    # 开启driver
    try:
        driver = webdriver.PhantomJS(executable_path='/Users/Dery/SeleniumWebDriver/phantomjs-2.1.1-macosx/bin/phantomjs')
        # 获得参数
        first_name = need_info_list[0]
        second_name = need_info_list[1]
        third_name = need_info_list[2]
        cate_url = need_info_list[3]
        time.sleep(2)
        driver.get(cate_url)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        company_name_list = soup.select('div.material ul li > dl > dd > p.padL200 > a')

        lock.acquire()
        for company_name in company_name_list:
            all_category_info.write(first_name+'\t'+second_name+'\t'+third_name+'\t'+cate_url+'\t'+company_name.text.strip()+'\t'+'http://ck.buildnet.cn'+company_name['href'].strip()+'\n')
            print(company_name.text)
            all_category_info.flush()
        lock.release()

        total_page_list = soup.select('div#pagerList')[0].text
        total_page = int(total_page_list.split('/')[1].split(' ')[0])
        if total_page != 1:
            for page in range(total_page-1):
                time.sleep(1)
                driver.find_element_by_css_selector('#pagerList a:nth-of-type({})'.format(page+2)).click()
                soup_next = BeautifulSoup(driver.page_source,'html.parser')
                company_next_name_list = soup_next.select('div.material ul li > dl > dd > p.padL200 > a')
                lock.acquire()
                print(page+2)
                for company_name in company_next_name_list:
                    all_category_info.write(first_name+'\t'+second_name+'\t'+third_name+'\t'+cate_url+'\t'+company_name.text.strip()+'\t'+'http://ck.buildnet.cn'+company_name['href'].strip()+'\n')
                    print('next page',company_name.text)
                    all_category_info.flush()
                lock.release()
        driver.close()
        driver.quit()
    except Exception as e:
        print(e)
        driver.quit()

def get_all_info_by_phantomJS(need_info_list):
    try:
        # driver = webdriver.PhantomJS(executable_path='/Users/Dery/phantomjs-2.1.1-macosx/bin/phantomjs')
        # 获得参数
        first_name = need_info_list[0]
        second_name = need_info_list[1]
        third_name = need_info_list[2]
        cam_url = need_info_list[3]
        campany_name = need_info_list[4]
        campany_url = need_info_list[5]
        driver.get(campany_url)
        driver.save_screenshot(campany_name+'.png')
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        address = soup.select('#contenl > div.c.basInf > dl > dd:nth-of-type(1) > p')[0].text.strip()
        phone = soup.select('#contenl > div.c.basInf > dl > dd:nth-of-type(2) > p')[0].text.strip()
        mail = soup.select('#contenl > div.c.basInf > dl > dd:nth-of-type(4) > p')[0].text.strip()
        print(address)
        lock.acquire()
        all_category_info_all.write(first_name+'\t'+second_name+'\t'+third_name+'\t'+cam_url+'\t'+campany_name+'\t'+campany_url+'\t'+address+'\t'+phone+'\t'+mail+'\n')
        all_category_info_all.flush()
        lock.release()
        driver.close()
        # driver.quit()
    except Exception as e:
        print(e)
        driver.quit()

def handle_basic():
    global lock,all_category_info
    lock = Lock()
    all_category_url = open('all_category_url.csv','r')
    all_category_info = open('all_category_info.csv','w')

    category_info_list = []
    for all_category in all_category_url.readlines():
        first_name = all_category.split('\t')[0]
        second_name = all_category.split('\t')[1]
        third_name = all_category.split('\t')[2]
        url_name = all_category.split('\t')[3].strip()
        category_info_list.append((first_name,second_name,third_name,url_name))

    pool = Pool(10)
    pool.map(get_all_company_by_phantomJS,category_info_list)
    pool.close()
    pool.join()
    all_category_info.close()

def handle_info():
    global lock,all_category_info_all,driver
    lock = Lock()
    # driver = webdriver.PhantomJS(executable_path='/Users/Dery/SeleniumWebDriver/phantomjs-2.1.1-macosx/bin/phantomjs')
    driver = webdriver.Chrome(executable_path='/Users/Dery/SeleniumWebDriver/chromedriver')
    driver.get('http://pass.buildnet.cn/auth/greennkit')
    # driver.get('http://pass.buildnet.cn/auth/greennkit?redirect=http%3a%2f%2fck.buildnet.cn%2fMain%2fEnterprise%2f533634%3fEID%3d533634%26state%3d8dcb399bebd045d8b00d2f208176e876')
    # driver.set_window_size(1124, 850)
    driver.save_screenshot('login_picture.png')
    # # get image
    # soup = BeautifulSoup(driver.page_source,'html.parser')
    # code_img = soup.select('#img-checkcode')[0]['src']
    # code_img_url = 'http://pass.buildnet.cn'+code_img
    # print(code_img_url)
    # with open('code_img.jpg','wb') as code_img_file:
    #     code_img_file.write(requests.get(code_img_url).content)
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
    all_category_url = open('all_category_info_basic.csv','r')
    all_category_info_all = open('all_category_company_info.csv','w')
    category_cam_list = []
    for all_category in all_category_url.readlines():
        first_name = all_category.split('\t')[0]
        second_name = all_category.split('\t')[1]
        third_name = all_category.split('\t')[2]
        cate_url = all_category.split('\t')[3]
        campany_name = all_category.split('\t')[4].strip()
        campany_url = all_category.split('\t')[5].strip()
        #--------------------
        try:
            print(campany_url)
            driver.get(campany_url)
            time.sleep(3)
            # driver.save_screenshot(campany_name+'.png')
            soup = BeautifulSoup(driver.page_source,'html.parser')
            address = soup.select('#contenl > div.c.basInf > dl > dd:nth-of-type(1) > p')[0].text.strip()
            phone = soup.select('#contenl > div.c.basInf > dl > dd:nth-of-type(2) > p')[0].text.strip()
            # mail = soup.select('#contenl > div.c.basInf > dl > dd:nth-of-type(4) > p')[0].text.strip()
            print(address)
            # lock.acquire()
            all_category_info_all.write(first_name+'\t'+second_name+'\t'+third_name+'\t'+cate_url+'\t'+campany_name+'\t'+campany_url+'\t'+address+'\t'+phone+'\n')
            all_category_info_all.flush()
            # lock.release()
            # driver.close()
            # driver.quit()
        except Exception as e:
            print(e)
        #     driver.quit()

        # category_cam_list.append((first_name,second_name,third_name,cate_url,campany_name,campany_url))
    #
    # pool = Pool(10)
    # pool.map(get_all_info_by_phantomJS,category_cam_list)
    # pool.close()
    # pool.join()
    all_category_info_all.close()
    # driver.quit()


if __name__ == '__main__':

    # handle_basic()
    # 去重
    # import os
    # os.system('sort -u ' + 'all_category_info.csv' + ' > ' + 'all_category_info_basic.csv')

    handle_info()
