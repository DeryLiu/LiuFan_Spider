import urllib.request
import requests
#python3x中,urllib2改成了urllib.request

mmurl = 'https://mm.taobao.com/json/request_top_list.htm?type=0&page='
#这个是一个淘宝模特信息的一个网址
i = 0
ph = -1
temp = '''"<img src"'''
while i < 4:
    url = mmurl + str(i)
    up = requests.get(url)
    cont = up.text
    print('-------------------------------')
    #需要从网页中找到图片的地址
    '''
    head = "<img src"
    tail = ".jpg"
    ph = cont.find(bytes(head, 'UTF-8'))
    pj = cont.find(bytes(tail, 'UTF-8'), ph + 1)
    print(cont[ph + len(temp):pj + len(tail)])
    '''
    print('-------------------------------')

    ahref = "<a href"
    target = "target"
    pa = cont.find(bytes(ahref,'UTF-8')) #需要转码,用bytes(,'UTF-8')转
    pt = cont.find(bytes(target,'UTF-8'),pa)
    # print(cont[pa + (len(ahref)) + 2 : pt - 2])
    http = "http:"
    bhttp = bytes(http,'UTF-8')
    modelurl = bhttp + cont[pa + (len(ahref)) + 2 : pt - 2]
    mup = urllib.request.urlopen(modelurl)
    mcont = mup.read()
    print(mcont)
    i += 1
