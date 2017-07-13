import codecs
import json
import re
from Tools import get_html
import time
import pytz
import random
from datetime import datetime,timedelta
from Tools.AMAZON_API.amazon_api.Amazon_api import Amazon_MWS,Amazon_AWS
from multiprocessing import Pool,Lock
from Tools import ALL_CONFIG
#把list洗乱
def shuffle_list(list_name):

    from random import shuffle
    shuffle(list_name)
    # 返回随机排序后的序列
    return list_name

'''Amazon API'''
def get_product_infos(asins,fail_url):
    global fr
    # global ferr
    fr = open('./Result/result.txt', 'aw')
    result = amazon_aws.get_product_info(asins)

    # result_dict = result
    if result['result']:
        # print result['data']
        fr.write(str(result['data'])+'\n')
        result_dict = result['data']
    else:
        print ('not', str(result['error_message']))
        # ferr.write(str(asins) + '\t' + str(result['error_message']) + '\n')
        with open('./Result/fail_url.txt','aw') as fail_url:
            fail_url.write(fail_url+'\n')
        result_dict = {}
    return result_dict

#传入商品页面的html和商品的id
def get_info(html, itemsurl):

    #----
    is_Refurbished = False
    #
    items_json = {'registered_land': '', 'isbn': '', 'description': '', 'weight': '0.0000', 'ean': '', 'mpn': '',
                  'key_name': ' ', 'price': '', 'height': '0.0000', 'currency': 'USD', 'brand': '',
                  'length_class': '', 'product_id': '', 'category': '','jan': '', 'seller_id': '', 'name': '',
                  'keyword': '', 'weight_class': 'kg', 'url': '','key_attribute': '','detail': {}, 'shipping': '',
                  'orders': 0, 'reviews': '0', 'width': '0.0000', 'length': '0.0000','location': '',
                  'attributes': [{'price': '', 'variation_id': '', 'dictory': 'Ships From',
                                  'attributes': {'Ships From': ''}, 'image': [], 'quantity': 99}],
                  'category_id_path': '', 'category_id': '', 'upc': '', 'image': []}
    # items_info = []

    # ------------itemsId------------
    # print '----------------isbn--------------'
    itemsId_list = re.findall(r'/dp/(.*?)/ref', itemsurl, re.S)
    itemsId = ''.join(itemsId_list)
    isbn = str(str(itemsId))
    items_json['isbn'] = isbn
    # print itemsId

    # print '----------------product_id--------------'
    items_json['product_id'] = isbn


    #调用api
    result_response = get_product_infos(itemsId,itemsurl)

    print ('-==-=-=-==-=-=-=-=-=-=-')
    print (result_response)
    print ('-==-=-=-==-===-=-=-=-=-')

    # print ' ------------Price------------'
    try:
        price = re.findall(r'<span id="priceblock_ourprice" class="a-size-medium a-color-price">(.*?)</span>', html,re.S)[0]
        price = price.split('$')[1].replace('-','')
    except Exception:
        price_detail = result_response['detail']
        last_price = price_detail['ListPrice']
        price = last_price['FormattedPrice']
        price = price.split('$')[1]

    price = str(price)
    items_json['price'] = str(price)

    # print '----------------weight--------------'
    weight_number = 0.0000
    if result_response['detail'].has_key('PackageDimensions'):
        weight_number = result_response['detail']['PackageDimensions']['Weight']
    items_json['weight'] = weight_number

    # print '----------------height--------------'
    height_number = 0.0000
    if result_response['detail'].has_key('PackageDimensions'):
        height_number = result_response['detail']['PackageDimensions']['Height']
    items_json['height'] = height_number

    # print '----------------length--------------'
    length_number = 0.0000
    if result_response['detail'].has_key('PackageDimensions'):
        length_number = result_response['detail']['PackageDimensions']['Length']
    items_json['length'] = length_number

    # print '----------------length_class--------------'
    length_class = 'cm'
    items_json['length_class'] = length_class

    # print '----------------category--------------'
    category_html_list = re.findall(r'<ul class="a-unordered-list a-horizontal a-size-small">(.*?)</ul>',html,re.S)
    category_list = re.findall(r'<a class="a-link-normal a-color-tertiary" .*?>(.*?)</a>',str(category_html_list),re.S)

    category_string_path = ''
    for category in category_list:
        category = str(category).replace('\\n','').replace(' ','')
        category_string_path = category_string_path + category + '>'
    items_json['category'] = category_string_path[:-1]

    print ('----------------category_id_path--------------')
    category_id_path =''
    category_id_path_api =  result_response['category'][::-1]
    for category in category_id_path_api:
        category_id_path = category_id_path + category + '>'

    items_json['category_id_path'] = category_id_path[:-1]

    print ('----------------category_id----------------')
    items_json['category_id'] = str(result_response['category'][::-1][-1])

    # print '----------------upc--------------'
    items_json['upc'] = result_response['detail']['UPC']


    # print '----------------seller_id--------------'
    sellerId = ''
    items_json['seller_id'] = sellerId

    # print '----------------weight_class--------------'
    weight_class = 'kg'
    items_json['weight_class'] = weight_class

    # print '----------------width--------------'
    width_number = 0.0000
    if result_response['detail'].has_key('PackageDimensions'):
        width_number = result_response['detail']['PackageDimensions']['Width']
    items_json['width'] = width_number

    # print '----------------url--------------'
    url = itemsurl
    # url = items_info['url']
    items_json['url'] = url

    # print '----------------shipping--------------'
    shipping = 0.0000
    items_json['shipping'] = shipping

    # print '------------Stock------------'
    # is_stock = True
    # try:
    #     stock_info_list = re.findall(r'<span class="a-size-medium a-color-success">(.*?)</span>',html,re.S)
    #     stock_info = re.findall(r'[A-Z].*k',str(stock_info_list),re.S)
    #     if stock_info:
    #         stock = stock_info
    #         is_stock = True
    #     else:
    #         stock = 'None'
    #         is_stock = False
    #   #  items_info['stock'] = stock
    # except Exception:
    #     stock = 'Fail'
    #
    # items_info.append(str(stock))

    # print ' ------------brand------------'

    brand = result_response['brand']
    items_json['brand'] = brand

    # print ' ------------title------------'
    title = result_response['title']
    title = str(title).replace('//','')
    items_json['name'] = title

    if str(title).find("Refurbished") == -1 or str(title).find("used") ==-1:
        is_Refurbished = False
    else:
        is_Refurbished = True

    # print '------------Reviews------------'
    # review = ''
    # review_count = re.findall(r'<span id="acrCustomerReviewText" class="a-size-base">(.*?)</span>',html,re.S)
    # print review_count+'======'
    # review = str(review_count).split(' ')[0]
    # items_json['reviews'] = review

    # print ' ------------image------------'
    image_list = result_response['image_list']
    if image_list == []:
        image_list = ['','','','','']
    while len(image_list) < 5:
        image_list.append("")

    # print type(image_list)
    images = image_list[:5]  # 最多取5张图片
    # items_info +=
    items_json['image'] = images

    # print '----------------attributes----------------'
    items_json['attributes'][0]['price'] = str(price)
    items_json['attributes'][0]['variation_id'] = itemsId + '_' + itemsId
    items_json['attributes'][0]['image'] = images[0]

    # print '----------------description-------短描-------'
    # 前有\xe2\x9c\x94     \xc2\xa0
    description_str = ''
    details_Feature = result_response['detail']
    details_list = details_Feature['Feature']

    if isinstance(details_list, str):
        details_list = [details_list]
        print (details_list)

    while len(details_list)<4:
        details_list.append("")

    details_list = details_list[:4]
    for i in range(0,4):
        details_list[i] = str(details_list[i]).replace('\n','').replace('\xe2\x9c\x94','').replace('\xc2\xa0','').replace('<br>','.').replace('</br>','')
        description_str = description_str+details_list[i]+';'
        if str(details_list[i]).find("Refurbished") == -1 or str(details_list[i]).find("used") == -1:
            is_Refurbished = False
        else:
            is_Refurbished = True
    items_json['description'] = description_str

    # print '----------------detail----------详描----'
    # ------------Specification------------
    Specification = result_response['description']
    if Specification == None or len(Specification)>5000:
        Specification = ''
    # if len(Specification)  <5000:
    #     Specification = Specification[:2000]
    # Specification = ''.join(Specification)
    # Specification = str(Specification).replace('\n','').replace('\xe2\x9c\x94','').replace('\xc2\xa0','').replace('<b>','').replace('</b>','').replace('<br>','').replace('</br>','').replace('<br/>','')
    print ('12312312132123')
    print (Specification)

    items_json['detail'] = {'description':str(Specification)}

    print (items_json['detail'])

    if str(Specification).find("Refurbished") == -1 or str(Specification).find("used") == -1:
        is_Refurbished = False
    else:
        is_Refurbished = True

    print ('=====================END===================================')
    json_file = json.dumps(items_json)
    print (items_json)
    result_file.write(json_file + '\n')

    # if is_Refurbished == False:
    #     result_file.write(json_file + '\n')

    # if choice == 'y':
    #stock为None也写入文件
    # Certified Refurbished
    #     if is_Refurbished == False:
    #         result_file.write(json_file + '\n')
    #        # result_file.write("\t".join(items_info) + "\n")
        # else:
        #     pass
    # else:
        # if is_stock:
        #     if is_Refurbished == False:
        #         result_file.write(json_file + '\n')
        #      #   result_file.write("\t".join(items_info) + "\n")
            # else:
            #     pass
        # else:    # stock为None不写入文件
        #
        #     with open('./Result/fail_url.txt','aw') as fail_url:
        #         fail_url.write(itemsurl+'\n')

    print ('=============')
    # f.flush()
    item_file.flush()
    result_file.flush()


#把itemsId页面的html传入get_info函数中，把失败的id重新存一个文件
def handle(itemsurl):
    time.sleep(0.5)
    try:
        #商品详情页
        #获取每一个商品页面的html
        html = get_html.get_amazon_html_proxy(itemsurl)
        # print html
        # 获取每一个商品的asin

        if html:
            #调用get_info函数，传入html
            get_info(html,itemsurl)
        else:
            with open(ALL_CONFIG.AMAZON_FAIL_HTML_FILE, 'aw') as h:
                h.write(itemsurl + '\n')

    except Exception as e:
        # print itemsurl, ":",  e
        with open(ALL_CONFIG.AMAZON_FAIL_URL_FILE,'aw') as fail_url:
            fail_url.write(itemsurl+'\n')
        # with open('./Result/no_except.txt', 'aw') as f:
        #     f.write(itemsurl + '\n')

#把items_last.txt文件中的字段制成表格
def create_titles(filename, titles):
    f = open(filename, "w")
    f.write("\t".join(titles) + "\n")
    #清除内部缓冲区
    f.flush()
    #关闭文件
    f.close()

#去重后的items的id文件
def start(items_file):

    global result_file, lock, titles,fr,ferr,item_file
    item_file = open(items_file, 'r')
    #调用函数create_titles
    result_file = open(ALL_CONFIG.AMAZON_DB_ITEMS_FILE, 'aw')
    items_list = item_file.readlines()
    #把获取的url依次传入handle
    items = []
    for item in items_list:
        item = item.split('\n')[0]
        items.append(item)
    lock = Lock()
    pool = Pool(10)
    #调用函数把items的url依次传入handle函数中爬虫
    pool.map(handle, items)
    pool.close()
    pool.join()

    item_file.close()
    result_file.close()

if __name__ == "__main__":
    #获取api的response
    to_time = str(datetime.now(pytz.UTC) - timedelta(hours = 2)).split('.')[0].replace(' ','T') + 'Z'
    print ('start:',datetime.now(pytz.UTC))
    from_time = str(datetime.now(pytz.UTC) - timedelta(days = 1)).split('.')[0].replace(' ','T') + 'Z'
    amazon_mws = Amazon_MWS()
    amazon_aws = Amazon_AWS()
    # start_api()
    t = datetime.now(pytz.UTC)

    # choice = raw_input('Need None(y/n)?\n')

    start(ALL_CONFIG.AMAZON_DB_URL_FILE)
