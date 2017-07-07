import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool,Lock
'''
字段：公司名称、联系人、地址、电话、邮箱、主营产品。
'''

def get_city_url():
    url = 'http://www.joojcc.com/company/'
    city_url = open('city_url.csv','w')
    with open('text.html','r') as text_file:
        soup = BeautifulSoup(text_file.read(),'html.parser')
        all_area = soup.select('div.conE.companyCity > ul li a')
        for area in all_area:
            # print(area)
            print(area['href'],area.text)
            city_url.write(area.text+','+'http://www.joojcc.com'+area['href']+'\n')

def handle_all_url():
    global lock,company_url_file,error_file
    lock = Lock()
    company_url_file = open('company_url.csv','w')
    city_url_file =  open('city_url.csv','r')
    error_file = open('error.csv','w')
    city_url_tuple = []
    for city_url in city_url_file.readlines():
        city_name = city_url.split(',')[0]
        city_main_url = city_url.split(',')[1].strip()
        city_url_tuple.append((city_name,city_main_url))
    pool = Pool(20)
    pool.map(get_all_url,city_url_tuple)
    pool.close()
    pool.join()
    company_url_file.close()
    error_file.close()

def get_all_url(info_tuple_list):
    city_name = info_tuple_list[0]
    city_main_url = info_tuple_list[1]
    # print(city_name,city_main_url)
    try:
        req1 = requests.get(city_main_url.format(1))
        req1.encoding = 'gb2312'
        soup1 = BeautifulSoup(req1.text,'html.parser')
        page_count = int(soup1.select('div.conD.companyList > div > div')[0].text.split('共')[1].split('页')[0].strip())

        company_info_list = soup1.select('div.conD.companyList > ul > li > h1 > b > a')
        for company_info in company_info_list:
            company_name = company_info.text
            company_url = company_info['href']
            lock.acquire()
            company_url_file.write(city_name+','+company_name+','+company_url+'\n')
            company_url_file.flush()
            lock.release()
            print(company_name)

        if page_count !=1:
            company_url_list = [city_main_url.format(page+1) for page in range(1,page_count)]
            for com_url in company_url_list:
                req = requests.get(com_url)
                req.encoding = 'gb2312'
                soup = BeautifulSoup(req.text,'html.parser')
                company_info_list = soup.select('div.conD.companyList > ul > li > h1 > b > a')
                for company_info in company_info_list:
                    company_name = company_info.text
                    company_url = company_info['href']
                    lock.acquire()
                    company_url_file.write(city_name+','+company_name+','+company_url+'\n')
                    company_url_file.flush()
                    lock.release()
                    print(company_name)
    except Exception as e:
        lock.acquire()
        error_file.write(city_name+','+city_main_url+'\n')
        error_file.flush()
        lock.release()
        print(e)

handle_all_url()