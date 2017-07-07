import requests,re,time
from bs4 import BeautifulSoup
from multiprocessing import Pool,Lock
'''
字段：公司名称、联系人、地址、电话、邮箱、主营产品。
'''

def handle_all_url():
    global lock,company_info_file,error_file
    lock = Lock()
    company_url_file = open('company_url.csv','r')
    company_info_file =  open('company_info_all.csv','w')
    error_file = open('error.csv','w')
    city_url_tuple = []
    for city_url in company_url_file.readlines():
        city_name = city_url.split(',')[0]
        company_name = city_url.split(',')[1]
        company_url = city_url.split(',')[2].strip()
        city_url_tuple.append((city_name,company_name,company_url))
    pool = Pool(20)
    pool.map(get_all_url,city_url_tuple)
    pool.close()
    pool.join()
    company_info_file.close()
    error_file.close()

def get_all_url(info_tuple_list):
    city_name = info_tuple_list[0]
    company_name = info_tuple_list[1]
    company_url = info_tuple_list[2]
    # print(city_name,city_main_url)
    try:
        req = requests.get(company_url)
        req.encoding = 'gb2312'
        soup = BeautifulSoup(req.text,'html.parser')
        company_info_list = str(soup.select('#mainLeft > div.contact > ul li'))
        info_list = re.findall('<li>(.*?)</li>',company_info_list,re.S)
        company_contact,company_address,company_tel,company_phone = '','','',''
        main_major = '&'.join(soup.select('#mainRight > div.conA.info > ul > li')[-1].span.text)
        for info in info_list:
            if '联 系 人：' in info:
                company_contact = re.findall('<span>(.*?)</span>',info,re.S)[0]
                # print(company_contact)
            if '公司地址：' in info:
                company_address = re.findall('<span>(.*?)</span>',info,re.S)[0]
                # print(company_address)
            if '公司电话：' in info:
                company_tel = re.findall('<span>(.*?)</span>',info,re.S)[0].split(' ')[0].strip()+'-'+re.findall('<span>(.*?)</span>',info,re.S)[0].split(' ')[-1]
                # print(company_tel)
            if '手 机：' in info:
                company_phone = re.findall('<span>(.*?)</span>',info,re.S)[0]

        lock.acquire()
        company_info_file.write(city_name+','+company_name+','+company_contact+','+company_phone+','+company_tel+','+company_address+','+main_major+'\n')
        company_info_file.flush()
        lock.release()
        print(company_contact)

    except Exception as e:
        lock.acquire()
        error_file.write(city_name+','+company_name+','+company_url+'\n')
        error_file.flush()
        lock.release()
        print(e)



handle_all_url()
