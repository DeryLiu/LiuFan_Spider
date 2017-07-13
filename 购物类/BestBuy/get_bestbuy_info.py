import re
from Tools import get_html,ALL_CONFIG
import random
import requests
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

def get_info(file_name):
    global false, true, null
    false = False
    true = True
    null = None

    file_id = open("./Id_last.txt", "r")
    titles = ['itemsId', 'price', 'Original_price', 'ship', 'stock', 'brand', 'title', 'img1', 'img2', 'img3',
              'img4','img5', 'detail1', 'detail2', 'detail3', 'detail4', 'detail5','Specification']

    # 调用函数create_titles
    create_titles(file_name, titles)

    Ids = file_id.readlines()

    # result_file = open(result_file, "aw")
    # with open('./Result/items.xls','aw') as f:
    for goods_id in Ids:
        goods_id = goods_id.split("\n")[0]
        # print goods_id
        url = 'http://api.bestbuy.com/v1/products/' + str(goods_id) + '.json?apiKey=68zbtdy4wmac9dgvnbhwke4e'
        info = get_html.get_html_src(url)
        # 将字符串str当成有效的表达式来求值并返回计算结果，即去掉引号
        items_info = eval(info)
        itemsId = items_info['sku']
        # print itemsId

        goods_info = []

        goods_info.append(str(itemsId))

        #售价
        price = items_info['salePrice']
        goods_info.append(str(price))
        #一般价
        Original_price = items_info['regularPrice']
        goods_info.append(str(Original_price))
        #ship
        ship = items_info['shippingCost']
        if ship == '':
            ship = "Null"
        goods_info.append(str(ship))
        #stock
        stock_info = items_info['onlineAvailability']
        #判断是否有库存
        if stock_info:
            stock = 'in stock'
        else:
            stock = 'out of stock'
        goods_info.append(str(stock))

        #brand
        brand = ''
        if items_info.has_key('manufacturer'):
            brand = items_info['manufacturer']
        goods_info.append(str(brand))

        #title
        title = items_info['name']
        goods_info.append(str(title))

        #image
        url = 'http://www.bestbuy.com/site/products/' + str(goods_id) + '.p'
        html = get_html.get_html_src(url)
        img_list = re.findall(r'<li data-target="#carousel-main".*?src="(.*?);', html, re.S)
        while len(img_list) < 5:
            # for img_info in img_list:
            #     if img_info.find("Image coming soon") == -1:
            #         img_list = []
            #     else:
            img_list.append("")

        # print len(img_list)
        imgs = img_list[:5]  # 最多取8张图片
        # imgs = [8]
        # for i in range(8):
        #     imgs[i] = img_list[i]
        # print "-=-=-=-=-=-=-=-=-=-="
        # print imgs
        # print "-=-=-=-=-=-=-=-=-=-="
        goods_info += imgs

        # detail = ''
        detail_url = 'http://www.bestbuy.com/site/searchpage.jsp?st='+goods_id+'&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys'
        detail_html = get_html.get_html_src(detail_url)
        # print detail_html

        detail_list = []

        detail_list_src = re.findall(r'<div class="short-description">(.*?)</div>', detail_html, re.S)
        if detail_list_src ==[]:
            detail_list.append('Brand Type:'+ brand)
        # print detail_list_src
        if detail_html:
            for detail_items in detail_list_src:
                # print detail_items
                detail_list = re.findall(r'<li>(.*?)</li>', detail_items, re.S)
                if detail_list ==[]:
                    detail_list = detail_list_src
                # print "--------------"
                # print detail_list
                # detail_list.append(dtmp1)


            while len(detail_list) < 5:
                detail_list.append("")
            # print len(img_list)
            detail_info= detail_list[:5]  # 最多取8张图片
            goods_info += detail_info

        # if items_info.has_key('shortDescription'):
        #     detail = items_info['shortDescription']
        # print goods_id

        # print "-=-=-=-=-=-=-=-=-=-="
        # print detail
        # print "-=-=-=-=-=-=-=-=-=-="


        # # feature
        # if items_info.has_key('longDescription'):
        #     feature_info = items_info['longDescription']
        #     if len(feature_info) > 500:
        #         feature_info = str(feature_info[:500])
        # else:
        #     feature_info = ""
        # # print len(feature_info)
        #
        # goods_info.append(str(feature_info))
        #     # print feature_info

        #spct
        spct_info = re.findall(r'data-tabs=.*?fragmentUrl&quot;:&quot;(.*?);', html, re.S)
        # 1139003

     # data-tabs=
     # "[{&quot;fragmentUrl&quot;:&quot;/site/kodak-pixpro-sp360-hd-action-camera-aqua-sport-pack-yellow/1139003.p

        if spct_info:
            spct_url = 'http://www.bestbuy.com' + spct_info[0]+";template=_specificationsTab"

        # spct_info = re.search(r'data-tabs=.*?"(.*?)"', html, re.S)
        # if spct_info:
        #     spct_all = spct_info.group(1)
        #     spct_list = spct_all.replace('&quot;', '"')
        #     spct_list = eval(spct_list)
        #     spct_url_info = spct_list[1]['fragmentUrl']
        #     spct_url = 'http://www.bestbuy.com' + str(spct_url_info)

            html1 = get_html.get_html_src(spct_url)

         #   spct_html = re.findall(r'<div class="specification-title">Key Specs</div>.*?<div class="header">(.*?)</div>.*?<div class="specification-value">(.*?)</div>.*?<i class="fistack info-icon">.*?<div class="header">(.*?)</div>.*?<div class="specification-value">(.*?)</div>.*?<div class="specification-name"><span>(.*?)</span>.*?<div class="specification-value">(.*?)</div>', html1, re.S)
            #spct_html = re.findall(r'<div class="specification-group key-specs">.*?<div class="specification-name">(.*?)</div>.*?<div class="specification-value">(.*?)</div>.*?<div class="specification-group">',html1)
            spct_html_limit = re.findall(r'<div class="specification-group key-specs">(.*?)<div class="specification-group">',html1,re.S)
            spct_html = re.findall(r'<div class="specification-name">(.*?)</div>.*?<div class="specification-value">(.*?)</div>',str(spct_html_limit),re.S)

            spct_dic = {}
            if spct_html:
                for spct_items in spct_html:
                    tmp1 = re.sub(r'<[^>]+>', '', spct_items[0], re.S)
                    # print "tmp1"
                    # print tmp1

                    retmp1 = tmp1.replace('&nbsp;','')
                    tmp2 = spct_items[1]
                    # print "tmp2"
                    # print tmp2
                    spct_dic[retmp1] = tmp2
                    # print "spct_dic"
                    # print spct_dic
            spct_dic = str(spct_dic)
            # print "---------------"
            # print spct_dic
        else:
            spct_dic = ""

        goods_info.append(spct_dic)
        # print goods_info
        # spct_len = len(spct_dic)
        # if spct_len > 2000:
        #     spct_dic = spct_dic[:2000]  # 如何字符长度大于2000，则取前面2000个字符
        # info['Specification'] = spct_dic

        # # spct_all = spct_info.group(1)
        # spct_list = spct_info.replace('&quot;', '"')
        # spct_list = eval(spct_list)
        # spct_url_info = spct_list[1]['fragmentUrl']
        # spct_url = 'http://www.bestbuy.com' + str(spct_url_info)
        # print spct_url

        #     feature_list = feature_info.split('.')
        #     feature = feature_list
        #     feature = ['detail1', 'detail2', 'detail3', 'detail4', 'detail5']
        #     feature_len = len(feature)
        #     features = detail
        #     feature_count = len(features)
        #     if feature_count < feature_len:
        #         features += ['' for _i in range(feature_len - feature_count)]
        #     feature_dict = dict(zip(feature, features))
        # return feature_dict

        # spct_info = re.findall(r'data-tabs=[\s]"(.*?)"', html, re.S)
        # pct_url = 'http://www.bestbuy.com' + str(spct_url_info)

        # print len(goods_info)

        # write info to file

        result_file.write("\t".join(goods_info) + "\n")

        print ('=============')
        print (goods_info)

        # f.flush()
        file_id.flush()
        result_file.flush()

    # with open("./Result/items.xls", "aw") as f:
    #     try:
    #         f.write("\t".join(goods_info) + "\n")
    #         print goods_info
    #         f.close()
    #     except Exception, e:
    #         print str(e)


if __name__ == "__main__":
    global result_file,file_name
    # file_name = './Result/Video Game/Xbox 360/Xbox 360.xls'
    file_name = './Result/2-in-1s1.xls'
    result_file = open(file_name,'aw')

    get_info(file_name)

    # send_email(result_file)


