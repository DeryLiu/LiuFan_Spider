import json
import re
# import get_html
import random
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from Tools import ALL_CONFIG

def get_html_src(url):
    """
    get page source
    :param url:
    :return:
    """
    with open(ALL_CONFIG.USER_AGENT_FILE) as f:
        try:
            header_list = f.readlines()
            # ASIN = asin.split("\n")[0]
            # header = "User-Agent:" + random.choice(header_list)

        except Exception as e:
            print (str(e))
    # count = 0
    while True:
        try:
            header = {"User-Agent": random.choice(header_list).split("\n")[0]}
            # print header
            req = requests.get(url, None, header=header,timeout=10)
            html = req.text
            # robot_check = re.findall('<title dir="ltr">Robot Check</title>', html)
            # if robot_check and count < 6:
            #     count += 1
            return html
            # else:
            #     return html
        except Exception as e:
            print (str(e))
            # count += 1
            # if count > 5:
            # return

def get_info(file_name):
    global false, true, null
    false = False
    true = True
    null = None

    items_json = {'registered_land': '', 'isbn': '', 'description': '', 'weight': '0.0000', 'ean': '', 'mpn': '',
                  'key_name': ' ', 'price': '', 'height': '0.0000', 'currency': 'USD', 'brand': '',
                  'length_class': '', 'product_id': '', 'category': '','jan': '', 'seller_id': '', 'name': '',
                  'keyword': '', 'weight_class': 'kg', 'url': '','key_attribute': '','detail': {}, 'shipping': '',
                  'orders': 0, 'reviews': '0', 'width': '0.0000', 'length': '0.0000','location': '',
                  'attributes': [{'price': '', 'variation_id': '', 'dictory': 'Ships From',
                                  'attributes': {'Ships From': ''}, 'image': [], 'quantity': 99}],
                  'category_id_path': '', 'category_id': '', 'upc': '', 'image': []}

    file_id = open("./text_last.txt", "r")

    Ids = file_id.readlines()

    for goods_id in Ids:
        goods_id = goods_id.split("\n")[0]
        # print goods_id
        url = 'http://api.bestbuy.com/v1/products/' + str(goods_id) + '.json?apiKey=68zbtdy4wmac9dgvnbhwke4e'
        info = get_html_src(url)
        # 将字符串str当成有效的表达式来求值并返回计算结果，即去掉引号
        items_info = eval(info)

        # print '----------------isbn--------------'
        isbn = str(items_info['sku'])
        items_json['isbn'] = isbn

        # print '----------------brand--------------'
        brand = 'no brand'
        if items_info.has_key('manufacturer'):
            brand = items_info['manufacturer']
        items_json['brand'] = brand.replace('\xc2\xae','').replace('\xe2\x84\xa2','')

        # print '----------------description-------短描-------'
        # items_json['description'] = items_info['shortDescription']
        # detail = ''
        description_url = 'http://www.bestbuy.com/site/searchpage.jsp?st=' + goods_id + '&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys'
        description_html = get_html_src(description_url)
        # print detail_html

        description_list = []
        description_list_src = re.findall(r'<div class="short-description">(.*?)</div>', description_html, re.S)
        if description_list_src == []:
            description_list.append('Brand Type:' + brand)
        # print detail_list_src
        if description_html:
            for description_items in description_list_src:
                # print detail_items
                description_list = re.findall(r'<li>(.*?)</li>', description_items, re.S)
                if description_list == []:
                    description_list = description_list_src

            # print len(img_list)
            description_str = ''
            description_append = 'Brand Name:'+brand
            if len(description_list) <= 4:
                description_list = description_list[:3]
                description_list.append(description_append)
            for description in description_list:
                description_str = description_str + description + ';'
            # description_info = description_list[:4]
            # items_json['description'] = str(description_info).replace('\\xc2\\xae','').replace('\u00ae','').replace('\\xc2\\xae','')
            items_json['description'] = description_str.replace('\u00ae','').replace('\\xc2\\xae','').replace('\\xc2\\xae','').replace('\\\\','')

        # print '----------------weight--------------'
        # weight_number = 0.0000
        if items_info.has_key('weight'):
            if items_info['weight'] == null:
                weight_number = 0.0000
                items_json['weight'] = weight_number
            else:
                items_json['weight'] = str(items_info['weight']).split(' ')[0]


        # print '----------------price--------------'
        price = items_info['salePrice']
        items_json['price'] = str(price)

        # print '----------------height--------------'
        height_number = 0.0000
        if items_info.has_key('height'):
            if items_info['height'] == null:
                height_number = 0.0000
                items_json['height'] = height_number
            else:
                items_json['height'] = height_number

        # print '----------------length_class--------------'
        if items_info.has_key('depth'):
            if items_info['depth'] == null:
                length_class = 'cm'
            else:
                length_class = str(items_info['depth']).split(' ')[1]
            items_json['length_class'] = length_class

        # print '----------------product_id--------------'
        items_json['product_id'] = items_info['productId']

        # print '----------------category--------------'
        category_path = items_info['categoryPath']
        category_string_path = ''
        for category in range(1,len(category_path)):
            path_name = category_path[category]['name']
            category_string_path = category_string_path+path_name+'>'

        items_json['category'] = category_string_path[:-1]

        # print '----------------seller_id--------------'
        if items_info['sellerId'] == null:
            sellerId = ''
        else:
            sellerId = items_info['sellerId']
        items_json['seller_id'] = sellerId

        # print '----------------name--------------'
        name = str(items_info['name']).replace('\xc2\xae','').replace('\xe2\x84\xa2','')
        items_json['name'] = name

        # print '----------------weight_class--------------'
        if items_info.has_key('weight'):
            if items_info['weight']==null:
                weight_class = 'kg'
            else:
                weight_class = str(items_info['weight']).split(' ')[1]
            items_json['weight_class'] = weight_class

        # print '----------------url--------------'
        url = 'http://www.bestbuy.com/site/products/' + str(goods_id) + '.p'
        # url = items_info['url']
        items_json['url'] = url

        # print '----------------detail----------详描----'
        html = get_html_src(url)
        spct_info = re.findall(r'data-tabs=.*?fragmentUrl&quot;:&quot;(.*?);', html, re.S)

        if spct_info:
            spct_url = 'http://www.bestbuy.com' + spct_info[0] + ";template=_specificationsTab"
            html1 = get_html_src(spct_url)
            spct_html_limit = re.findall(
                r'<div class="specification-group key-specs">(.*?)<div class="specification-group">', html1, re.S)
            spct_html = re.findall(
                r'<div class="specification-name">(.*?)</div>.*?<div class="specification-value">(.*?)</div>',
                str(spct_html_limit), re.S)

            spct_dic = {}
            if spct_html:
                for spct_items in spct_html:
                    tmp1 = re.sub(r'<[^>]+>', '', spct_items[0], re.S)
                    retmp1 = tmp1.replace('&nbsp;', '')
                    tmp2 = spct_items[1]
                    spct_dic[retmp1] = tmp2
            spct_dic = str(spct_dic)
        else:
            # spct_dic = {}
            spct_dic = dict(name)

        # spct_dic = items_info['longDescription']
        items_json['detail'] = eval(spct_dic)
        # dictMerged2 = dict(dict1, **dict2)


        # print '----------------shipping--------------'
        items_json['shipping'] = items_info['shippingCost']

        # print '----------------reviews--------------
        if items_info.has_key('customerReviewCount'):
            if items_info['customerReviewCount'] == null:
                reviews = '0'
            else:
                reviews = items_info['customerReviewCount']
            items_json['reviews'] = reviews

        # print '----------------width--------------'
        items_json['width'] = str(items_info['width']).split(' ')[0]

        # print '----------------category_id_path--------------'
        category_id_path = ''
        for category in range(1,len(category_path)):
            path_name = category_path[category]['id']
            category_id_path = category_id_path+path_name+'>'

        items_json['category_id_path'] = category_id_path[:-1]

        # print '----------------category_id----------------'
        items_json['category_id'] = category_path[-1]['id']

        # print '----------------upc--------------'
        items_json['upc'] = items_info['upc']

        # print '----------------stock----------------'
        # stock_info = items_info['onlineAvailability']
        # #判断是否有库存
        # if stock_info == False:
        #     stock = '0'
        # if stock_info == True:
        #     stock = '1'

        # print '----------------image----------------'
        img_list = re.findall(r'<li data-target="#carousel-main".*?src="(.*?);', html, re.S)
        imgs = img_list[:5]  # 最多取5张图片
        items_json['image'] = imgs

        # print '----------------attributes----------------'
        items_json['attributes'][0]['price'] = str(price)
        items_json['attributes'][0]['variation_id'] = isbn+'_'+isbn
        items_json['attributes'][0]['image'] = img_list[0]
        # "attributes": [
        #     {"price": "", "variation_id": "", "dictory": "Ships From", "attributes": {"Ships From": ""}, "image": [],
        #      "quantity": 99}]

        # print '----------------写入文件----------------'
        json_file = json.dumps(items_json)
        result_file.write(json_file+'\n')
        print ('=============')
        print (items_json)

        file_id.flush()
        result_file.flush()

# def send_email(infofile):
#     #创建一个带附件的实例
#     msg = MIMEMultipart()
#     #构造附件1
#     att1 = MIMEText(open(infofile, 'rb').read(), 'base64', 'utf-8')
#     att1["Content-Type"] = 'application/octet-stream'
#     att1["Content-Disposition"] = 'attachment; filename="update_info_part.zip"'#这里的filename可以任意写，写什么名字，邮件中显示什么名字
#     msg.attach(att1)
#     #加邮件头 #发送给相关人员
#     # to_list=['hengwei@starmerx.com','jianmei@starmerx.com']
#     to_list=['hengwei@starmerx.com']
#     msg['to'] = ';'.join(to_list)
#     msg['from'] = 'hengwei@starmerx.com'
#     msg['subject'] = 'bestbuy抓取数据'
#     #发送邮件
#     try:
#         server = smtplib.SMTP()
#         server.connect('smtp.exmail.qq.com')
#         server.login('hengwei@starmerx.com','Lianyu2016')#XXX为用户名，XXXXX为密码
#         server.sendmail(msg['from'], to_list,msg.as_string())
#         print '发送成功',infofile
#     except Exception, e:
#         print '发送失败',e
#         #server.quit()
#         send_email(infofile)
#     finally:
#         server.quit()

if __name__ == "__main__":
    global result_file,file_name
    file_name = './Result/result_db.csv'
    result_file = open(file_name,'w')
    get_info(file_name)

    # send_email(result_file)


