from bs4 import BeautifulSoup
import time,pymysql
from multiprocessing import Pool,Lock
from selenium import webdriver
import requests,re,random
import http.cookiejar

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

# 保存每个分类下的'更多'的company页面
def get_cate_company_allCate():
    error_file = open('error_file1.csv','w')
    MaiGou_Cate_All = open('MaiGou_Cate_All.csv','w')
    # with open('MaiGou_Cate_url.csv','r') as MaiGou_Cate_url:
    with open('error_file.csv','r') as MaiGou_Cate_url:
        for MaiGou_Cate in MaiGou_Cate_url.readlines():
            first_cate,second_cate,cate_url = MaiGou_Cate.split(',')
            try:
                resonseLF = requests.get(cate_url.strip(),headers=get_headers())
                soup = BeautifulSoup(resonseLF.text,'html.parser')
                more_url = soup.select('#leftlayout > div > div.v2_brand_bangdan > div > div > div.blist > div > a')[0]['href']
                MaiGou_Cate_All.write(first_cate+','+second_cate+','+more_url+'\n')
                print(more_url)
            except Exception as e:
                error_file.write(first_cate+','+second_cate+','+cate_url)
                print(cate_url.strip(),e)

# get_cate_company_allCate()

# 获取公司url
def get_all_company_url():
    error_file = open('error_file.csv','w')
    MaiGou_Company_ulr = open('MaiGou_Company_URL11.csv','w')
    with open('MaiGou_Cate_All.csv','r') as MaiGou_caet:
        for Maigou in MaiGou_caet.readlines():
            first_cate,second_cate,more_url = Maigou.split(',')
            try:
                response = requests.get(more_url.strip(),headers=get_headers())
                soup = BeautifulSoup(response.text,'html.parser')
                img_lit = soup.select('#container > div.blockcont > div > div > ul > li > div.detail > div.td2 > div > img')
                title_list = soup.select('#container > div.blockcont > div > div > ul > li > div.simple > div.td2 > a')
                company_url = soup.select('#container > div.blockcont > div > div > ul > li > div.detail > div > div > div > a:nth-of-type(1)')
                for i in range(len(title_list)):
                    MaiGou_Company_ulr.write(first_cate+','+second_cate+','+company_url[i*2]['href']+','+title_list[i].text+','+img_lit[i]['src']+'\n')
                    print(company_url[i*2]['href'])
            except Exception as e:
                error_file.write(first_cate+','+second_cate+','+more_url)
                print(e)

# get_all_company_url()

# 公司信息
def get_company_info():
    db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    cursor=db.cursor()
    # driver = webdriver.Chrome(executable_path="/Users/Dery/SeleniumWebDriver/chromedriver")

    error_file = open('error_file_1.csv','w')
    # with open('MaiGou_Company_URL.csv','r') as MaiGou_caet:
    with open('error_file.csv','r') as MaiGou_caet:
        for Maigou in MaiGou_caet.readlines():
            first_cate,second_cate,more_url,short_name,logo = Maigou.split(',')
            # print(first_cate,second_cate,more_url,short_name,logo)
            c_url = more_url.replace('product_','').replace('news_','').replace('company/pl_','brand/').replace('shop_','')
            try:
                # driver.get(c_url)
                # soup = BeautifulSoup(driver.page_source,'html.parser')
                response = requests.get(c_url,headers=get_headers())
                soup = BeautifulSoup(response.text,'html.parser')
                c_info = ''.join(i.text for i in soup.select('#leftlayout > div > div.brandinfo > div.right > ul > li'))
                try:
                    company_name = soup.select('#leftlayout > div.swiperbox > div > div.companyinfo > ul > li.name')[0].text
                except:
                    company_name = short_name
                # print(company_name)
                company_info = ''.join([i.text.replace('\n','') for i in soup.select('#leftlayout > div.leftbg > div.introduce > div.desc')]).replace("'"," ")
                # print(company_info)
                try:
                    company_web = soup.select('#leftlayout > div.swiperbox > div > div.companyinfo > ul > li > a')[0].text
                except:
                    company_web = re.findall('>(.*?)</a>',c_info,re.S)[0]
                # print(company_web)

                c2_info = ''.join(i.text for i in soup.select('#companyinfo > div.b_company_info > div > div > div.b-botm > ul.license'))

                try:
                    mg_phone = re.findall('联系电话：(.*?)</li>',str(soup.select('#leftlayout > div.swiperbox > div > div.companyinfo > ul > li')),re.S)[0]
                except:
                    mg_phone = re.findall('联系电话：(.*?)\n',str(c2_info),re.S)[0]
                # print(mg_phone)

                try:
                    company_address = soup.select('#leftlayout > div.swiperbox > div > div.companyinfo > ul > li.address')[0].text
                except:
                    company_address = re.findall('企业地址：(.*?)\n',c2_info,re.S)[0]
                # print(company_address)

                try:
                    product_build_data = re.findall('品牌创立时间：(.*?)</li>',str(soup.select('div.brandinfo > div > ul > li')),re.S)[0]
                    # print(product_build_data)
                except:
                    product_build_data = ' '

                company_basic_info = soup.select('div.b_company_info > div > div')
                company_build_data = re.findall('企业成立日期：(.*?)<',str(company_basic_info),re.S)[0]
                # print(company_build_data)

                try:
                    resgin_money = re.findall('认缴注册资本：(.*?)<',str(company_basic_info),re.S)[0].split('(')[0]
                except:
                    resgin_money = '0'
                # print(resgin_money)

                # MG_Major = (' '.join(soup.select('div > div.votelist > div')[i].text for i in range(len(soup.select('div > div.votelist > div')))))
                # print(MG_Major)
                try:
                    MG_ID = re.findall('brand/(.*?).html',str(soup.select('#header > div > div.hmidbox > div.headsearch > div.search_left > a.index1')),re.S)[0]
                    MG_Major_URL = 'http://www.maigoo.com/ajaxstream/?do=loadblock&dataType=text&param=v2_brand_vote_brandid%3A{}_page%3A1'.format(MG_ID)
                    MG_response = requests.get(MG_Major_URL)
                    MG_soup = BeautifulSoup(MG_response.text,'html.parser')
                    MG_Major = ' '.join([i.text for i in MG_soup.select('div.votelist > div > a')])
                except:
                    MG_Major = ' '

                try:
                    news_url = soup.select('#leftlayout > div.swiperbox > div > div > div > div > div.more > a')[5]['href']
                except:
                    news_url = ''
                # print(news_url)
                # print(company_name+','+company_web+','+'logo url'+','+product_build_data+','+MG_Major+','+news_url+','+company_address+','+mg_phone+','+company_build_data+','+resgin_money+','+company_info)
                insert_sql = "INSERT INTO `MaiGou`(first_cate,second_cate,company_name,company_url,logo_url,product_build_data,mg_major,news_url,address,mg_phone,build_date,resg_money,mg_info) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(first_cate,second_cate,company_name,company_web,logo.strip(),product_build_data,MG_Major,news_url,company_address,mg_phone,company_build_data,resgin_money,company_info)
                try:
                    cursor.execute(insert_sql)
                    db.commit()
                    print(short_name,' -insert')
                except Exception as e:
                    db.rollback()
                    print(insert_sql,e)
            except Exception as e:
                error_file.write(first_cate+','+second_cate+','+more_url+','+short_name+','+logo)
                print(c_url,e)


# 公司新闻
def get_company_news_first():
    db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    cursor=db.cursor()
    with open('MaiGou_News_Url.csv','r') as MaiGou_news_file:
        for MaiGou_news in MaiGou_news_file.readlines():
            first_cate,second_cate,company_name,news_url_a = MaiGou_news.split(',')
            try:
                MG_Response = requests.get(news_url_a,headers=get_headers())
                soup = BeautifulSoup(MG_Response.text,'html.parser')
                news_title_list = soup.select('div.news > div.rowlist > div.item div.info ul li span a.linka')
                for i in news_title_list:
                    news_title = i.text
                    news_url = i['href']
                    if 'news' in news_url:
                        news_info = ' '
                        insert_sql = "INSERT INTO `MaiGou_News`(first_cate,second_cate,company_name,news_url,news_title,news_info) VALUES ('{}','{}','{}','{}','{}','{}')".format(first_cate,second_cate,company_name,news_url.strip(),news_title,news_info)
                        try:
                            cursor.execute(insert_sql)
                            db.commit()
                            print(' -insert')
                        except Exception as e:
                            db.rollback()
                            print(insert_sql,e)
            except Exception as e:
                print(company_name,e)


def get_company_news_last():
    error_file = open('error_file.csv','r')
    db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
    cursor=db.cursor()
    # select_sql = 'SELECT * FROM MaiGou_News;'
    # cursor.execute(select_sql)
    # for i in cursor.fetchall():
    for i in error_file.readlines():
        # mg_id,first_cate,second_cate,company_name,news_url,news_title = i
        # print(mg_id,first_cate,second_cate,company_name,news_url,news_title)
        news_url,news_title = i.split(',')

        # print(company_name,news_url,news_title)
        try:
            MG_Response = requests.get(news_url,headers=get_headers())
            soup = BeautifulSoup(MG_Response.text,'html.parser')
            try:
                description = soup.select('div.description')[0].text
            except:
                description = ''

            news_info_f = ''.join(i.text.strip() for i in soup.select('div.articlecont > div p'))
            if news_info_f == '':
                news_info_f = ''.join(i.text.strip() for i in soup.select('div div.md_word p'))

            news_info_l = description+news_info_f
            # print(news_info_l)
            update_sql = "UPDATE MaiGou_News SET news_info='{}' WHERE news_url='{}' AND news_title='{}';".format(news_info_l.strip().replace("'","‘").replace('"','”'),news_url,news_title.strip())
            try:
                cursor.execute(update_sql)
                db.commit()
                print(' -update')
            except Exception as e:
                db.rollback()
                print(update_sql,e)
        except Exception as e:
            # error_file.write(first_cate+','+second_cate+','+company_name+','+news_url+','+news_title+'\n')
            print(e)


if __name__ == '__main__':
    # get_company_news_first()
    get_company_news_last()
