import requests
from bs4 import BeautifulSoup
import re,random

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

Cate26 = open('category_26.txt','r')
error_file = open('error_file.csv','w')
with open('Cate26_Top20.csv','w') as Top_20:
    for cate in Cate26.readlines():
        fq_cate,mg_cate,mg_url = cate.split(',')
        cate_id = re.findall('daquan_(.*?).html',mg_url,re.S)[0]
        for page in range(1,3):
            url = 'http://www.maigoo.com/ajaxstream/?do=loadblock&dataType=text&param=v2_brand_daquancol1_catid%3A{}_num%3A10_page%3A{}_autopage%3A2&ajaxload=1'.format(cate_id,page)
            try:
                res = requests.get(url,headers=get_headers())
                soup = BeautifulSoup(res.text,'html.parser')

                logo_list = soup.select('div > div.img > a > img')
                # print(logo_list)
                brand_list = soup.select('div > div.info > div > a')
                # print(brand_list)
                for i in range(len(logo_list)):
                    rank = (i+1)+(page-1)*10
                    logo = logo_list[i]['src']
                    brand = brand_list[i].text
                    Top_20.write(fq_cate+','+mg_cate+','+str(rank)+','+logo+','+brand+'\n')
                    print(brand)
            except:
                error_file.write(fq_cate+','+mg_cate+','+mg_url+','+page+'\n')
    # res = requests.get(url)
    # soup = BeautifulSoup(res.text,'html.parser')
    #
    # rank_num_list = soup.select('#container > div.blockcont > div:nth-of-type(1) > div > ul > li.trans100 > div.td1 > div')
    # # print(rank_num_list)
    # brand_name = soup.select('#container > div.blockcont > div:nth-of-type(1) > div > ul > li.trans100 > div.detail > div.td3 > div > div.dhidden > a:nth-of-type(1)')
    # # print(brand_name)
    # company_name = soup.select('#container > div.blockcont > div:nth-of-type(1) > div > ul > li.trans100 > div.detail > div.td3 > div > div.dhidden')
    # # print(re.findall('\((.*?)\)',company_name[0].text,re.S)[0])
    #
    # for i in range(len(rank_num_list)):
    #     FangChan.write(rank_num_list[i].text+','+brand_name[i].text+','+re.findall('\((.*?)\)',company_name[i].text,re.S)[0]+'\n')
    #
    # for i in range(2,34):
    #     url_list = url_conten.format(i)
    #     resxu = requests.get(url_list)
    #     soup_xu = BeautifulSoup(resxu.text,'html.parser')
    #
    #     rank_num_xu = soup_xu.select('li.trans100 > div.td1 > div.tbcell')
    #     brand_name_xu = soup_xu.select('li.trans100 > div.simple > div.td2 > a')
    #     company_name_xu = soup_xu.select('li.trans100 > div.simple > div.td3 > div')
    #     # print(rank_num_xu)
    #     # print(brand_name_xu)
    #     # print(company_name_xu[2].text.split(' ')[0].strip())
    #     for i in range(len(rank_num_xu)):
    #         FangChan.write(rank_num_xu[i].text+','+brand_name_xu[i].text+','+company_name_xu[i].text.split(' ')[0].strip()+'\n')
    #
