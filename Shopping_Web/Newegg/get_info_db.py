import codecs
import json
from multiprocessing import Pool, Lock
import re
from Tools import get_html,ALL_CONFIG

#把list洗乱
def shuffle_list(list_name):

    from random import shuffle
    shuffle(list_name)
    # 返回随机排序后的序列
    return list_name

#传入商品页面的html和商品的id
def get_info(html, itemsId):

    items_json = {'registered_land': '', 'isbn': '', 'description': '', 'weight': '0.0000', 'ean': '', 'mpn': '',
                  'key_name': ' ', 'price': '', 'height': '0.0000', 'currency': 'USD', 'brand': '',
                  'length_class': '', 'product_id': '', 'category': '', 'jan': '', 'seller_id': '', 'name': '',
                  'keyword': '', 'weight_class': 'kg', 'url': '', 'key_attribute': '', 'detail': {}, 'shipping': '',
                  'orders': 0, 'reviews': '0', 'width': '0.0000', 'length': '0.0000', 'location': '',
                  'attributes': [{'price': '', 'variation_id': '', 'dictory': 'Ships From',
                                  'attributes': {'Ships From': ''}, 'image': [], 'quantity': 99}],
                  'category_id_path': '', 'category_id': '', 'upc': '', 'image': []}

    #读取价格字段存入
    # price = re.findall("<meta itemprop='price' content='(.*?)'", html)[0]
    # items_json['price'] = price

    # print '----------------isbn--------------'
    items_json['isbn'] = itemsId

    # print '----------------price--------------'
    url = 'http://www.newegg.com/Product/MappingPrice2012.aspx?Item=' + itemsId
    html_price = get_html.get_html(url)
    price = re.findall('<span class="price-was-data" style="display: none">(.*?)</span>', html_price)
    if price:
        price = price[0]
    else:
        price = 'None'
    items_json['price'] = price

    # print '----------------url--------------'
    items_json['url'] = url

    # print '----------------shipping--------------'
    ship = '0'
    ship = re.search(r'product_default_shipping_cost:\[(.*?)\]', html)
    if ship:
        ship = ship.group(1).replace("'", "")
    items_json['shipping'] = ship

    # print '----------------brand--------------'
    brand = ''
    brand = re.search(r'product_manufacture:\[(.*?)\]', html)
    if brand:
        brand = brand.group(1).replace("'", "")
    items_json['brand'] = brand

    # print '----------------name--------------'
    name = ''
    name_info = re.search(r'product_title:\[(.*?)\]', html)
    if name_info:
        name = name_info.group(1).replace("'", "").replace('&amp;', '').replace("#34;", "''").replace("#40;",
                                                                                                      "(").replace(
            '#41;', ')').replace("#47;", "\\")
        name = name.decode("ascii").encode("utf-8")
    items_json['name'] = name

    # print '----------------weight--------------'
    weight_number = 0.0000
    items_json['weight'] = weight_number

    # print '----------------weight_class--------------'
    weight_class = 'kg'
    items_json['weight_class'] = weight_class

    # print '----------------height--------------'
    height_number = 0.0000
    items_json['height'] = height_number

    # print '----------------width--------------'
    width = 0.0000
    items_json['width'] = width

    # print '----------------length_class--------------'
    length_class = 'cm'
    items_json['length_class'] = length_class

    # print '----------------product_id--------------'
    items_json['product_id'] = itemsId

    # print '----------------reviews--------------
    reviews = '0'
    items_json['reviews'] = reviews

    # print '----------------upc--------------'
    upc = ''
    items_json['upc'] = upc


    # print '----------------seller_id--------------'
    sellerId = ''
    items_json['seller_id'] = sellerId

    # print '----------------detail----------详描----'
    Specification = {}
    spct_info = re.search(r'<div id="Specs" class=.*?>(.*?)</div>', html, re.S)
    if spct_info is not None:
        spct_info = spct_info.group(1)
        spct_list = re.findall(r'<dl><dt>(.*?)</dt><dd>(.*?)</dd></dl>', spct_info, re.S)
        if spct_list:
            for spct in spct_list:
                temp1 = re.sub(r'<[^>]+>', '', spct[0], re.S)
                temp2 = re.sub(r'<[^>]+>', '', spct[1], re.S)
                Specification[temp1] = temp2
    items_json['detail'] = Specification

    # Specification = str(Specification).replace('{', '').replace('}', '').replace("'", '').replace(',','').replace('<br>','')
    # if len(items_info['Specification']) >= 2000:
    #     items_info['Specification'] = items_info['Specification'][0:1999]

    image = []
    image_info = re.search(r'"imageSetImageList":"(.*?)"', html, re.S)
    image_list = ''
    if image_info is not None:
        image_list = image_info.group(1)
        image_all = image_list.split(',')
        for images in image_all:
            images = 'http://images17.newegg.com/is/image/newegg/' + images
            image.append(images)
    if image_info is None:
        image_info = re.search(r'"imageNameList":"(.*?)"\}', html, re.S)
        if image_info is not None:
            image_list = image_info.group(1)
            image_all = image_list.split(',')
            for images in image_all:
                if images != '"dfis360ImgFlag":"':
                    images = images.split('"')[0]
                    images = 'http://images10.newegg.com/ProductImage/' + images
                    image.append(images)
    items_json['image'] = image

    category_dict = {'Computer Systems':'ID-CS-503','Components':'ID-C-504','Electronics':'ID-E-505','Gaming':'ID-G-506','Networking':'ID-N-507',
                     'Office Solutions':'ID-OS-508','Software Services':'ID-SS-509','Automotive Industrial':'ID-AI-510','Home Tools':'ID-HT-511',
                     'Health Sports':'ID-HS-512','Apparel Accessories':'ID-AA-513','Hobbies Toys':'ID-HT-514'}

    # print '----------------category--------------'
    category_string_html = re.findall(r'<div id="baBreadcrumbTop" style="max-width:1420px; margin:0px auto;">(.*?)</div>', html, re.S)
    category_html_list = re.findall(r'title="(.*?)"', str(category_string_html), re.S)
    print (category_html_list)
    category_string = ''
    for category_s in category_html_list[2:]:
        category_string = category_string + category_s + '>'
    items_json['category'] = category_string[:-1]

    # print '----------------category_id_path--------------'
    category_url_list = re.findall(r'href="(.*?)"',str(category_string_html),re.S)
    category_id_path= ''
    for url_path in category_url_list:
        url_path = url_path.split('?')[0]
        category_id_path = category_id_path + url_path.split('/')[-1] + '>'
    items_json['category_id_path'] = str(category_dict[category_html_list[2]])+category_id_path[7:-1]

    # print '----------------category_id----------------'
    items_json['category_id'] = category_id_path.split('>')[-2]

    # print '----------------attributes----------------'
    items_json['attributes'][0]['price'] = str(price)
    items_json['attributes'][0]['variation_id'] = itemsId + '_' + itemsId
    items_json['attributes'][0]['image'] = image[0]

    # print '----------------description-------短描-------'
    details = []
    description_str = ''
    detail_info = re.search(r'<ul class="itemColumn">(.*?)</ul>', html, re.S)
    if detail_info is not None:
        detail_info = detail_info.group(1)
        detail_info = detail_info.replace('\r\n', '').replace('\t', '')
        detail = re.findall(r'<li.*?>(.*?)</li>', detail_info, re.S)
        for i in detail:
            i = i.strip()
            i = i.decode("ascii").encode("utf-8")
            details.append(i)
    #函数get_feature_dict
    for description in details:
        description_str = description_str + description + ';'
    items_json['description'] = description_str

    # print '----------------写入文件----------------'
    json_file = json.dumps(items_json)
    result_file.write(json_file + '\n')
    print ('=============')
    print (items_json)
    result_file.flush()

    # for k in titles:
    #     if items_dict.has_key(k):
    #         value = items_dict.get(k)
    #     else:
    #         value = 'None'
    #     lock.acquire()
    #     result_file.write(str(value) + "\t")
    #     result_file.flush()
    #     lock.release()
    #
    # lock.acquire()
    # result_file.write('\n')
    # result_file.flush()
    # lock.release()

#把itemsId页面的html传入get_info函数中，把失败的id重新存一个文件
def handle(itemsId):
    try:
        #删除itemsId开头结尾处的空格
        itemsId = itemsId.strip()
        #商品详情页
        url = 'http://www.newegg.com/Product/Product.aspx?Item=' + itemsId
        #获取每一个商品页面的html
        html = get_html.get_html(url)

        if html:
            #调用get_info函数，传入html和每个商品的id
            get_info(html, itemsId)
        else:
            with open('./get_html_fail.txt', 'aw') as h:
                h.write(itemsId + '\n')

    except Exception as e:
        print (itemsId, ":",  e)
        with open('./except.txt', 'aw') as f:
            f.write(itemsId + '\n')


#去重后的items的id文件
def start(items_file):

    global result_file, lock, titles

    item_file = open(items_file, 'r')

    result_file = open('./items_db.csv', 'w')
    items_list = item_file.readlines()
    lock = Lock()
    pool = Pool(10)
    #调用函数把items_list的内容依次传入handle函数中
    pool.map(handle, items_list)
    pool.close()
    pool.join()

    item_file.close()
    result_file.close()


if __name__ == "__main__":
    start('./items_db_last.txt')
