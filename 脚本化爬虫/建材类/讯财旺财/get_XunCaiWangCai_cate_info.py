import requests
from bs4 import BeautifulSoup

url = 'http://www.xuncaiwangcai.com/'
html_file = requests.get(url).text
with open('XCWC_Company_all_cate.csv','w') as sss:
    soup = BeautifulSoup(html_file,'html.parser')
    fir_cate = soup.select('h3 a')
    # print(fir_cate[0].a.text)
    for i in range(len(soup.select('h3'))):
        # ss = soup.select('#yw0 > div > div > div.item.item_red.item{:02} > div > div.subitem > ul > li'.format(i+1))
        sec_cate_list = soup.select('#yw0 > div > div > div.item.item_red.item{:02} > div > div.subitem > div'.format(i+1))
        # if len(sec_cate_list)>1:
        #     third_cate_list = soup.select('#yw0 > div > div > div.item.item_red.item14 > div > div.subitem > ul:nth-child(5)')
        third_cate_list = soup.select('#yw0 > div > div > div.item.item_red.item{:02} > div > div.subitem > ul li'.format(i+1))
        for thir in third_cate_list:
            one = soup.select('h3')[i].text.replace('\n\n\n','').replace('\n','&')
            two = sec_cate_list[0].text
            three = thir.text
            four = thir.a['href']
            sss.write(one+'\t'+two+'\t'+three+'\t'+four+'\n')