import random
import re
from selenium import webdriver
import requests
from Tools import ALL_CONFIG

def get_headers(host):
    #模拟浏览器
    user_agent_file = open(ALL_CONFIG.USER_AGENT_FILE, "r")
    # user_agent_list.close()
    user_agent_list = user_agent_file.readlines()
    user_agent = random.choice(user_agent_list).split("\n")[0]
    user_agent_file.close()
    try:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "en-US,en;q=0.8",
            # "Avail-Dictionary": "Dn5_GnWS",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": 'bby_rdp=l; intl_splash=false; testBucket=3; testMonetate=true; sn.ts=s||o~rs||64.402; bby_ab_search=a; abt609=c; abt629=a; s_sq=%5B%5BB%5D%5D; bby_cbc_lb=p-browse-e; mt.v=2.1942822343.1466585116121; s_vi=[CS]v1|2BB52809852AB740-40000301600177B0[CE]; akaau=1466645545~id=e99d6be7d36274231b65f0262a71403d; ltc=%20; track={"lastSearchTerm":"categoryid%24pcmcat144700050004","listFacets":"Condition%3ANew"}; s_cc=true; context_id=a89e17b8-3855-11e6-92da-0aebad99b5b7; context_session=c86df89c-38d7-11e6-aa83-0a93505c656d; s_fid=778D073F1CC2E786-0B721BA5100913D7; c2=Audio%3A%20Headphones%3A%20All%20Headphones%3A%20Faceted',
            "Host": host,
            "Upgrade-Insecure-Requests": "1",
            # "User-Agent": user_agent
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        }
        # print headers
        return headers
    except Exception as e:
        print (str(e))

#获取url页面的html
def get_html(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
        }
        req = requests.get(url, headers=headers,timeout=20)
        html = req.text
        return html
    except Exception as e:
        print (str(e))


def get_html_src(url):
    host = ''
    headers = get_headers(host)
    html = None
    count = 0
    while True:
        try:
            req = requests.get(url, None, headers=headers,timeout=20)
            html = req.text
            return html
        except Exception as e:
            print (str(e))
            count += 1
        while count > 5:
            return html


def get_html_proxy(url):
    headers = get_headers()
    html = None
    count = 0
    proxy_list = open(ALL_CONFIG.PROXY_LIST_FILE,'r')
    proxy = proxy_list.readlines()

    while True:
        try:
            proxy_support = {"http": "http://" + random.choice(proxy).split("\n")[0]}
            req = requests.get(url,headers=headers,proxy=proxy_support,timeout=20)
            html = req.text

            return html
        except Exception as e:
            print (str(e))
            count += 1
        while count > 5:
            return html

def get_amazon_html_proxy(url):
    host = 'www.amazon.com'
    headers = get_headers(host)
    html = None
    count = 0

    proxy_list = open(ALL_CONFIG.PROXY_LIST_FILE,'r')
    proxy = proxy_list.readlines()

    while True:
        try:
            proxy_support = {"http": "http://" + random.choice(proxy).split("\n")[0]}
            req = requests.get(url,headers=headers,proxy=proxy_support,timeout=20)
            html = req.text
            robot_check = re.findall('<title dir="ltr">Robot Check</title>', html)
            if robot_check:
                count += 1
            else:
                return html
        except Exception as e:
            print (str(e))
            count += 1
        while count > 5:
            return html

def get_PhantomJS_html(url):
    driver = webdriver.PhantomJS(executable_path=ALL_CONFIG.PHANTOMJS_PATH)
    driver.get(url)
    return driver.page_source  # 这就是返回的页面内容了

def post_data_html(url):
    import urllib.parse
    import urllib.request

    url = 'http://localhost/login.php'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    values = {
              'act' : 'login',
              'login[email]' : 'yzhang@i9i8.com',
              'login[password]' : '123456'
             }
    headers = { 'User-Agent' : user_agent }

    data = urllib.parse.urlencode(values)
    req = urllib.request.Request(url, data, headers)
    response = urllib.request.urlopen(req)
    the_page = response.read()

    print(the_page.decode("utf8"))