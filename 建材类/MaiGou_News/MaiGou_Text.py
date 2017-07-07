from bs4 import BeautifulSoup
import re


# MaiGou_cate = open('MaiGou_Cate_url.csv','w')
# with open('MaiGou_Text.html','r') as MaiGou_Text:
#     soup = BeautifulSoup(MaiGou_Text.read(),'html.parser')
#     llll = soup.select('#leftmenubg > ul > li:nth-of-type(1) > div > div.hotcategorybox')
#     second = re.findall('<dt>(.*?)</dt>',str(llll),re.S)
#     third = re.findall('<dd>(.*?)</dd>',str(llll),re.S)
#     # print(third)
#     for i in range(len(second)):
#         second_cate = re.findall('>(.*?)<',second[i],re.S)
#         print(second_cate)
#         third_cate = re.findall('"_blank">(.*?)</a>',third[i],re.S)
#         third_url = re.findall('href="(.*?)"',third[i],re.S)
#         for j in range(len(third_cate)):
#             MaiGou_cate.write(second_cate[0].replace(',',' ')+','+third_cate[j].replace(',',' ')+','+third_url[j].replace(',',' ')+'\n')
#             print(third_cate[j],third_url[j])

with open('MaiGou_Text.html','r') as MaiGou_Text:
    soup = BeautifulSoup(MaiGou_Text.read(),'html.parser')
    # logo_list = soup.select('#leftlayout > div.brandlist > div > div.rowlist > div > div.img > a > img')
    # print(logo_list)
    # brand_name = soup.select('#leftlayout > div.brandlist > div > div.rowlist > div > div.info > div > a')

    logo_list = soup.select('div > div.img > a > img')
    # print(logo_list)
    brand_list = soup.select('div > div.info > div > a')
    # print(brand_list)
    for i in range(len(logo_list)):
        print((i+1)+0*10)
        print(logo_list[i]['src'])
        print(brand_list[i].text)