from bs4 import BeautifulSoup
import requests,pymysql,random,time
import http.cookiejar
from multiprocessing import Pool,Lock
from selenium import webdriver

def get_url():
    GuangCai_Company_file = open('result.csv','w')
    driver = webdriver.Chrome(executable_path='/Users/Dery/SeleniumWebDriver/chromedriver')

    url_list = ['http://www.cali-light.com/cali/hyjs/list_122_{}.html'.format(i+1) for i in range(45)]
    for url in url_list:
        time.sleep(5)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        url_info = soup.select('div.ibox_2 > div.title_7_list > ul > li > a')
        for info in url_info:
            print(info['href'])
            GuangCai_Company_file.write(info['href']+'\n')

a = ['公司名称','负责人','电话','地址','传真']

def get_info():

    info_file = open('result.csv','r').readlines()
    with open('info_1.csv','w') as result:
        for url in info_file:
            try:
                req = requests.get(url.strip())
                req.encoding = 'gb2312'
                soup = BeautifulSoup(req.text,'html.parser')
        # with open('aaa.html','r') as sss:
        #     soup = BeautifulSoup(sss.read(),'html.parser')
                aa = soup.select('div.title_6_list table tr td')
                company_name = aa[2].text.strip()
                address = aa[4].text.strip()
                people = aa[8].text.strip()
                phone = aa[10].text.strip()
                tax = aa[12].text.strip()
                result.write(company_name+','+address+','+people+','+phone+','+tax+'\n')
                print(company_name,address,people,phone,tax)
            except Exception as e:
                print(url)
                print(e)

get_info()