from bs4 import BeautifulSoup
import requests
import re

# 十大品牌网的logo下载
def download_Pic():
    name_url_File = open('YunCaiGou.csv','r')
    for nameNurl in name_url_File.readlines():
        company_name,company_pic = nameNurl.split(',')
        try:
            response = requests.get(company_pic.strip())
            with open('./YunCaiGou/'+company_name+'.jpg','wb') as pic_name:
                pic_name.write(response.content)
                print(company_name)
        except:
            print(company_name,company_pic)

# '10.maigoo'
def maigoo10():
    'http://10.maigoo.com/list_1088.html'
    with open('maigoo10.csv','w') as maigoo10_file:
        try:
            response1 = requests.get('http://10.maigoo.com/list_1088.html')
            soup = BeautifulSoup(response1.text,'html.parser')
            img_lit1 = soup.select('#container > div.blockcont > div > div > ul > li > div > div > div > img')
            title_list1 = soup.select('#swhere > dl:nth-of-type(2) > dd > a')
            for i in range(len(title_list1)):
                maigoo10_file.write(title_list1[i].text+','+img_lit1[i]['src']+'\n')
                print(title_list1[i].text)
        except:
            print('page 1')

        url_list = ['http://10.maigoo.com/search/?blockid=3&catid=1088&C2464=4636&action=ajax&getac=brand&page={}'.format(i) for i in range(2,7)]
        for url in url_list:
            try:
                response2 = requests.get(url)
                soup2 = BeautifulSoup(response2.text,'html.parser')
                img_lit2 = re.findall('<img height="60" src="(.*?)" width="138"/>',str(soup2.select('div img')),re.S)
                title2 = soup2.select('li > div.simple > div.td3 > div')
                for j in range(len(title2)):
                    maigoo10_file.write(title2[j].text.strip()+','+img_lit2[j]+'\n')
                    print(title2[j].text.strip())
            except:
                print(url)

# 'http://www.maigoo.com/news/406333.html'
def maigoo500_imgURL():
    '''
    group_url_img_list = soup.select('table > tbody > tr > td > a')
    for i in range(len(group_url_img_list)):
        print(group_url_img_list[i].text,group_url_img_list[i]['href'])
    '''
    MaiGou500_Img = open('MaiGou500_Img.csv','w')
    error_file = open('error_file.csv','w')
    with open('MaiGou500.csv','r') as MaiGou500:
        for MaiGou in MaiGou500.readlines():
            company_name,company_url = MaiGou.split(',')
            try:
                response = requests.get(company_url.strip(),timeout=60)
                soup = BeautifulSoup(response.text,'html.parser')
                try:
                    group_img = soup.select('#leftlayout > div.leftbg > div.brandinfo > ul > li > a.img > img')[0]['src']
                except:
                    group_img = soup.select('#leftlayout > div.swiperbox > div > div.brandinfo > ul > li > a.img > img')[0]['src']
                MaiGou500_Img.write(company_name+','+group_img+'\n')
                print(group_img)
            except Exception as e:
                error_file.write(company_name+','+company_url)
                print(company_name)


# 'https://www.mycaigou.com/developer.html'
def YunCaiGou():
    YunCaiGou = open('YunCaiGou.csv','w')
    url_list = ['https://www.mycaigou.com/developer/page/{}.html'.format(i) for i in range(1,176)]
    for url in url_list:
        try:
            response = requests.get(url,timeout=60)
            soup = BeautifulSoup(response.text,'html.parser')
            group_img_name = soup.select('#content > div > div.developer_box > ul > li > div.developer_view > a > img')
            for i in range(len(group_img_name)):
                YunCaiGou.write(group_img_name[i]['alt']+','+group_img_name[i]['src']+'\n')
                print(group_img_name[i]['alt'],group_img_name[i]['src'])
        except:
            print('erroe',url)


# with open('PicPicPic.html','r') as PicPicPic:
#     url_list = ['https://www.mycaigou.com/developer/page/{}.html'.format(i) for i in range(1,176)]
#     print(url_list)
#
#     soup = BeautifulSoup(PicPicPic.read(),'html.parser')
#     group_img_name = soup.select('#content > div > div.developer_box > ul > li > div.developer_view > a > img')

# download_Pic()