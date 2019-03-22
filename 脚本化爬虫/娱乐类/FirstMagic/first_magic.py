#--*-- coding:utf-8 --*--
import requests,random
from bs4 import BeautifulSoup
import time
from selenium import webdriver

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
        'User-Agent': random.choice(USER_AGENTS),
    }
    return headers


# 1137个
def write_list():
    url_list = ['http://www.1moshu.com/forum-41-{}.html'.format(i) for i in range(1,58)]

    with open('magic_info.csv','w') as magic_info:
        for url in url_list:
            re = requests.get(url,headers=get_headers())
            re.encoding='gbk'

            soup = BeautifulSoup(re.text,'html.parser')
            magic_list = soup.select('a.z')
            # print(magic_list)
            for i in magic_list:
                magic_url = i['href']
                magic_name = i['title']
                print(magic_name+','+magic_url)
                magic_info.write(magic_name+','+magic_url+'\n')


headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'yDcp_2132_pc_size_c=0; yDcp_2132_saltkey=yCcFkC2w; yDcp_2132_lastvisit=1499749524; yDcp_2132_visitedfid=41; yDcp_2132_con_request_uri=http%3A%2F%2Fwww.1moshu.com%2Fconnect.php%3Fmod%3Dlogin%26op%3Dcallback%26referer%3Dhttp%253A%252F%252Fwww.1moshu.com%252Fforum-41-1.html; yDcp_2132_client_created=1499754278; yDcp_2132_client_token=33A335033264175B8C582EF5B7EC5CDF; yDcp_2132_ulastactivity=dcbb5Qr8qXHMwRN7SvGjNu%2BA7Es6TNWg2OwnwSAR1Lsvhzqi9gKf; yDcp_2132_auth=cad8DdSrgbG16tCXZ7HNrjMgvXZIRq50Y0z%2Bk0%2FDqcyRidAPi85KB%2FO7NPew%2BICxpXJ22ebGVnCp9FZ36PoURA; yDcp_2132_connect_login=1; yDcp_2132_connect_uin=33A335033264175B8C582EF5B7EC5CDF; yDcp_2132_stats_qc_login=3; yDcp_2132_security_cookiereport=22ccZfd5Ebdmq1pO9u6ezkBGIXSfx8R1dqCqn3TrMiD5M7SCtaxt; yDcp_2132_connect_last_report_time=2017-07-11; yDcp_2132_forumdefstyle=1; yDcp_2132_st_t=91%7C1499756354%7Cfdcee74d1047319a08c746d6263735f3; yDcp_2132_forum_lastvisit=D_41_1499756354; yDcp_2132_lip=180.173.172.195%2C1499755174; yDcp_2132_st_p=91%7C1499758723%7C8b17816985126b319a61f094bf6f3c1d; yDcp_2132_viewid=tid_11924; yDcp_2132_smile=1D1; yDcp_2132_sendmail=1; yDcp_2132_home_diymode=1; yDcp_2132_sid=XBV444; Hm_lvt_42e039744086ab82f6980bd5d614e894=1499752166; Hm_lpvt_42e039744086ab82f6980bd5d614e894=1499758978; yDcp_2132_checkpm=1; yDcp_2132_lastact=1499758979%09misc.php%09patch; yDcp_2132_connect_is_bind=1',
    'Host':'www.1moshu.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}

def get_pan_url():
    info_file = open('magic_info.csv','r')
    with open('magic_pan1.csv','w') as pan_file:
        for info in info_file.readlines()[125:]:
            magic_name,magic_url = info.split(',')
            time.sleep(0.8)
            re = requests.get(magic_url.strip(),headers=headers)
            re.encoding = 'gbk'
            soup = BeautifulSoup(re.text,'html.parser')
            magic_url = soup.select('dd.link2 > a')[0]['href']
            print(magic_url)
            pan_file.write(magic_name+','+magic_url+'\n')


def text():
    # url = 'http://www.1moshu.com/thread-3440-1-1.html'
    # re = requests.get(url,headers=headers)
    # re.encoding='gbk'
    #
    # with open('text1137.html','w') as tet:
    #     tet.write(re.text)

    with open('text1137.html') as text:
        soup = BeautifulSoup(text.read(),'html.parser')
        magic_list = soup.select('dd.link2 > a')
        print(magic_list[0]['href'])
        # for i in magic_list:
        #     magic_url = i['href']
        #     magic_name = i['title']
        #     print(magic_name+','+magic_url)


get_pan_url()
# text()