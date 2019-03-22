# http://www.jianshu.com/p/639a67bc75b9

from bs4 import BeautifulSoup
import urllib.request
import gzip
import inspect
import re
# import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool
import datetime
import sqlite3
from time import sleep
from random import choice

#用代理IP方式访问，见2.21部分
# conn=sqlite3.connect('/IPProxyPool/IPProxyPool_py2/data/proxy.db')
# IP = pd.read_sql("select* from proxys", conn)
# ip = [str(i) for i in IP['ip']]
# port = [str(i) for i in IP['port']]
# proxy = [ip[i] + ":" +port[i] for i in range(len(ip))]
proxy = ['120.76.79.21:80','120.92.237.69:80','101.4.136.34:81','112.91.135.115:8080', '112.91.135.115:8080']
proxy_support = urllib.request.ProxyHandler({'http':choice(proxy)})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)

#网页解压缩，见2.22部分
def read_zip_url(url):
    fails = 0
    while fails < 5:
        try:
            content = urllib.request.urlopen(url).read()
            content = gzip.decompress(content).decode("gb18030") #网页gb2312的编码要用这个
            break
        except:
            fails += 1
        print(inspect.stack()[1][3] + ' occused error')
    soup = BeautifulSoup(content, "html.parser")
    return soup

starturl = "http://zu.sh.fang.com/house/g22-n31/"
soup = read_zip_url(starturl)
area_first_soup = soup.find_all('dl',id = 'rentid_D04_01')[0].find_all('a')
del area_first_soup[-2]
del area_first_soup[0]
area_first = [] #注1
for i in area_first_soup:
    area_first.append("http://zu.sh.fang.com" + i.get('href'))

area_second = [] #注2
for i in area_first:
    soup = read_zip_url(i)
    area_second_soup = soup.find_all('div',id = 'rentid_D04_08')[0].find_all('a')
    del area_second_soup[0]
    for i in area_second_soup:
        area_second.append("http://zu.sh.fang.com" + i.get('href'))

area_third = [] #注3
def area_third_func(li):
    soup = read_zip_url(li)
    area_third_soup = soup.find_all('dl',id = 'rentid_D04_02')[0].find_all('a')
    del area_third_soup[0]
    for i in area_third_soup:
        area_third.append("http://zu.sh.fang.com" + i.get('href'))

pool = ThreadPool(4)
pool.map(area_third_func, area_second)
pool.close()
pool.join()

area_fourth = [] #注4
def area_fourth_func(li):
    soup = read_zip_url(li)
    if soup.find(text=re.compile("很抱歉")) == None:
        pagenum1 = soup.find_all('span', class_ = 'txt')[0].get_text()
        pagenum = int(re.findall(r'\d+',pagenum1)[0])
        splitted = li.split('-')
        for j in range(1, int(pagenum)+1):
            new_url = (splitted[0]+'{0}' + splitted[1] + '{0}' + splitted[2] + '{0}' + splitted[3] + '{0}' + splitted[4]+'{0}' + 'i3{1}'+'{0}' + splitted[5]).format('-',j)
            area_fourth.append(new_url)

pool = ThreadPool(4)
pool.map(area_fourth_func, area_third)
pool.close()
pool.join()

finalinks = [] #注5
def get_links(li):
    soup = read_zip_url(li)
    urlist = soup.select('a[href^="/chuzu/"]')
    for i in urlist:
        href = 'http://zu.sh.fang.com' + i.get('href')
        if href not in finalinks:
            finalinks.append(href)
    sleep(0.1)

pool = ThreadPool(4)
pool.map(get_links, area_fourth)
pool.close()
pool.join()

today = datetime.date.today().strftime("%Y%m%d")
# finalinks = pd.DataFrame(finalinks)
# finalinks = finalinks.drop_duplicates()
# finalinks.to_csv("%s" %'sf_links'+today + '.csv')
with open('{} sf_links'.format(today)+'.csv','w') as result_file:
    result_file.write(finalinks+'\n')