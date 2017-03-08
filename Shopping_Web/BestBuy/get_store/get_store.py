import pycurl
import urllib
import re
import random
from io import StringIO
import requests
from Tools import ALL_CONFIG,get_html
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

def create_titles(filename, titles):
    f = open(filename, "w")
    f.write("\t".join(titles) + "\n")
    #清除内部缓冲区
    f.flush()
    #关闭文件
    f.close()

def get_info(sku):
    global false, true, null
    false = False
    true = True
    null = None

    file_id = open("./test.json", "r")
    Ids = file_id.readlines()
    # result_file = open(result_file, "aw")
    # with open('./Result/items.xls','aw') as f:
    url = 'http://api.bestbuy.com/v1/products/' + sku[:-1] + '.json?apiKey=68zbtdy4wmac9dgvnbhwke4e'

    info = get_html.get_html_src(url)
    items_info = eval(info)
    if items_info.has_key("salePrice"):
        price = items_info['salePrice']
    else:
        price='wrong'

    a=Ids[0]
    m=eval(a)
    b=m['storeAvailabilities']
    myconf = {"ISSAQUAH WA":"0","TUKWILA WA":"0","FEDERAL WAY WA":"0","BELLEVUE WA":"0","SOUTH CENTER":"0",}
    mydata={}
    for li in b:

         if myconf.has_key(li['store']["name"]):
            if li['skuAvailabilities'][0].has_key("lowOnStock"):
                mydata[li['store']["name"]]="Low"
            else:
                mydata[li['store']["name"]]=li['skuAvailabilities'][0]["availabilityType"]

    realdata = myconf
    print (realdata)
    for (k,v) in mydata.items():

        realdata[k]=v
    realli=["2016-11-24",sku[:-1]]
    realli.append(str(price))
    state=''
    low=''
    donot=''
    nothave=''
    for (k,v) in realdata.items():
        if v=="InStore":
            v="3"
            state="1"
        elif v=='ShipToStore':
            v='1'
            donot="0"
        elif v=='Low':
            v="2"
            low="2"
        else:
            nothave='4'
        realli.append(v)
    if  state=="1":
        realli.append(state)
    elif state=='' and low=="2":
        realli.append(low)
    elif state=='' and low=='' and donot=='0':
        realli.append(donot)
    else:
        realli.append("4")
    print (realli)
    csv_writer.writerow(realli)

# 获取商品id
def getsku():
    # file_id = open("./store_last.txt", "r")
    file_id = open('./Result/tablets_last.txt','r')
    Ids = file_id.readlines()
    return Ids

def getstore(sku):
    url = "http://www.bestbuy.com/productfulfillment/api/1.0/storeAvailability/"
    post_data_dic = '{"skus":[{"skuId":'+sku+',"quantity":1}],"zipCode":"98031","customerUuid":null}'
    crl = pycurl.Curl()
    crl.setopt(pycurl.VERBOSE, 1)
    crl.setopt(pycurl.FOLLOWLOCATION, 1)
    crl.setopt(pycurl.MAXREDIRS, 5)
    # crl.setopt(pycurl.AUTOREFERER,1)

    crl.setopt(pycurl.CONNECTTIMEOUT, 60)
    crl.setopt(pycurl.TIMEOUT, 300)
    # crl.setopt(pycurl.PROXY,proxy)
    crl.setopt(pycurl.HTTPPROXYTUNNEL, 1)
    crl.setopt(pycurl.HTTPHEADER, ['Cookie: UID=863f53d8-ef16-46ef-affb-db56fa198d8b; bby_rdp=l; SID=d0e72f57-3b87-4579-b070-042a867c7d20; intl_splash=false; hfv4=b; testBucket=20; abt715=a; bby_ab_search=a; vt=2803556e-9ca6-11e6-a650-0e0457b797a6; pst2=839; __gads=ID=638032e963e38e63:T=1477614821:S=ALNI_MZI6bFL4tZt1dSVaGfb4oxixYDtzQ; sn.tfsonchat=status||false; sn.vi=vi||b193176f-6220-4426-9329-72cc70290ead; akaau=1477615568~id=9251fe5a6e80158dfde670df50e00ccd; track={"lastSearchTerm":"surface%20book","listFacets":""}; s_cc=true; mt.v=2.67814836.1477614799828; context_id=2dd07138-9ca6-11e6-bbf7-0e56d73d6d7b; context_session=2dd07340-9ca6-11e6-a409-0e56d73d6d7b; s_vi=[CS]v1|2C094E68052A92AC-400003010000E2B0[CE]; customerZipCode=98031|Y; sc-location=%7B%22value%22%3A%22%7B%5C%22zipCode%5C%22%3A%5C%2298031%5C%22%2C%5C%22storeId%5C%22%3A%5C%22839%5C%22%7D%22%2C%22meta%22%3A%7B%22CreatedAt%22%3A%222016-10-28T00%3A33%3A39.680Z%22%2C%22ModifiedAt%22%3A%222016-10-28T02%3A38%3A53.122Z%22%7D%7D; s_fid=26E3007F8B5D9B4A-0FC4F6207C8E3787; c2=Computers%20%26%20Tablets%3A%20Laptops%3A%20All%20Laptops%3A%20PC%20Laptops%3A%20pdp; s_sq=%5B%5BB%5D%5D','Origin: http://www.bestbuy.com','Accept-Encoding: gzip, deflate','Accept-Language: zh-CN,zh;q=0.8','User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36','Content-Type: application/json','Accept: */*','Referer: http://www.bestbuy.com/site/microsoft-surface-book-2-in-1-13-5-touch-screen-laptop-intel-core-i5-8gb-memory-128gb-solid-state-drive-silver/4530800.p?skuId=4530800','X-Requested-With: XMLHttpRequest','Connection: keep-alive'])
    crl.setopt(pycurl.COOKIE,'UID=863f53d8-ef16-46ef-affb-db56fa198d8b; bby_rdp=l; SID=d0e72f57-3b87-4579-b070-042a867c7d20; intl_splash=false; hfv4=b; testBucket=20; abt715=a; bby_ab_search=a; vt=2803556e-9ca6-11e6-a650-0e0457b797a6; pst2=839; __gads=ID=638032e963e38e63:T=1477614821:S=ALNI_MZI6bFL4tZt1dSVaGfb4oxixYDtzQ; sn.tfsonchat=status||false; sn.vi=vi||b193176f-6220-4426-9329-72cc70290ead; akaau=1477615568~id=9251fe5a6e80158dfde670df50e00ccd; track={"lastSearchTerm":"surface%20book","listFacets":""}; s_cc=true; mt.v=2.67814836.1477614799828; context_id=2dd07138-9ca6-11e6-bbf7-0e56d73d6d7b; context_session=2dd07340-9ca6-11e6-a409-0e56d73d6d7b; s_vi=[CS]v1|2C094E68052A92AC-400003010000E2B0[CE]; customerZipCode=98031|Y; sc-location=%7B%22value%22%3A%22%7B%5C%22zipCode%5C%22%3A%5C%2298031%5C%22%2C%5C%22storeId%5C%22%3A%5C%22839%5C%22%7D%22%2C%22meta%22%3A%7B%22CreatedAt%22%3A%222016-10-28T00%3A33%3A39.680Z%22%2C%22ModifiedAt%22%3A%222016-10-28T02%3A38%3A53.122Z%22%7D%7D; s_fid=26E3007F8B5D9B4A-0FC4F6207C8E3787; c2=Computers%20%26%20Tablets%3A%20Laptops%3A%20All%20Laptops%3A%20PC%20Laptops%3A%20pdp; s_sq=%5B%5BB%5D%5D')
    crl.setopt(10102, 'gzip, deflate')
    # crl.setopt(pycurl.SOCKTYPE_ACCEPT, 'application/json')
    # crl.setopt(pycurl.CONTENT_TYPE, 'application/json')
    crl.fp = StringIO.StringIO()
    crl.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1")

    # Option -d/--data <data>   HTTP POST data
    # print urllib.urlencode(post_data_dic)
    # print urllib.urlencode(post_data_dic)
    crl.setopt(crl.POSTFIELDS, post_data_dic)

    crl.setopt(pycurl.URL, url)
    crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
    crl.perform()
    # print type(crl.fp.getvalue())
    with open('test.json','w') as f:
        f.write(crl.fp.getvalue()+'\n')

if __name__=='__main__':
    # 获取商品id
    ids=getsku()
    global csv_writer, file_name
    # 生成的文件名
    # file_name = './Result/result_store.csv'
    file_name = './Result/tablets_store.csv'
    result_file = open(file_name, 'aw')
    import  csv
    csv_writer = csv.writer(result_file)
    titles = ['date','skuid','price','ISSAQUAH WA','TUKWILA WA','BELLEVUE WA','FEDERAL WAY WA','SOUTH CENTER','STATUS']
    # 调用函数create_titles
    create_titles(file_name, titles)
    for i in  range(len(ids)):
        print (ids[i])
        getstore(ids[i])
        get_info(ids[i])

    # send_email(file_name)
