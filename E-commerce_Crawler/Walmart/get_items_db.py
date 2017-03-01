import HTMLParser
import json
from multiprocessing import Pool, Lock
import re
import sys  # 引用sys模块进来，并不是进行sys的第一次加载
import requests
import reload
from Tools import get_html
reload(sys)  # 重新加载sys
sys.setdefaultencoding('utf8')


# def get_feature_dict(detail):  # 将列表形式特征字段转换成字典形式
#
#
#     feature = ['detail1', 'detail2', 'detail3', 'detail4', 'detail5']
#     feature_len = len(feature)
#     features = detail
#     feature_count = len(features)
#     if feature_count < feature_len:
#         features += ['' for _i in range(feature_len - feature_count)]
#     feature_dict = dict(zip(feature, features))
#     return feature_dict

def get_info(items_info):  # 得到字段信息
    # items_result = {'itemsId': '', 'price': '', 'ship': '', 'stock': '', 'image1': '', 'brand': '', 'title': '',
    #                 'product_attr': '', 'Specification': ''}

    items_json = {'registered_land': '', 'isbn': '', 'description': '', 'weight': '0.0000', 'ean': '', 'mpn': '',
                  'key_name': ' ', 'price': '', 'height': '0.0000', 'currency': 'USD', 'brand': '',
                  'length_class': '', 'product_id': '', 'category': '', 'jan': '', 'seller_id': '', 'name': '',
                  'keyword': '', 'weight_class': 'kg', 'url': '', 'key_attribute': '', 'detail': {}, 'shipping': '',
                  'orders': 0, 'reviews': '0', 'width': '0.0000', 'length': '0.0000', 'location': '',
                  'attributes': [{'price': '', 'variation_id': '', 'dictory': 'Ships From',
                                  'attributes': {'Ships From': ''}, 'image': [], 'quantity': 99}],
                  'category_id_path': '', 'category_id': '', 'upc': '', 'image': []}

    # print '----------------isbn--------------'
    sku = ''
    if items_info.has_key('itemId'):
        sku = items_info['itemId']
    items_json['isbn'] = sku

    # print '----------------product_id--------------'
    items_json['product_id'] = sku

    # print '----------------price--------------'
    price = ''
    if items_info.has_key('salePrice'):
        price = items_info['salePrice']
    items_json['price'] = str(price)


    items_url = 'http://www.walmart.com/ip/' + str(sku)
    item_html = ''
    try:
        items_html = get_html.get_html(items_url)
    except Exception as e:
        print (e)

    # stock = ''
    # if items_info.has_key('stock'):
    #     stock_info = items_info['stock']
    #     if stock_info == 'Not Available' or stock_info == 'Not available':
    #         stock = 'out of stock'
    #     if stock_info == 'Available':
    #         stock = 'in stock'
    # items_result['stock'] = stock

    # description=''
    # if items_info.has_key('longDescription'):
    #     feature_all=items_info['longDescription'].strip()
    #     html = HTMLParser.HTMLParser()
    #     feature_html = html.unescape(feature_all)
    #     feature_info=re.sub(r'<[^>]+>', '', feature_html)
    #     description=feature_info
    # if len(description)>=2000:#判断，如果字符大于2000个则取前2000个
    #     description=description[:2000]
    # items_result['description']=description

    # print '----------------shipping--------------'
    ship = '0'
    if items_info.has_key('standardShipRate'):
        ship = items_info['standardShipRate']
    items_json['shipping'] = ship

    # feature = ''
    # if items_info.has_key('shortDescription'):
    #     feature = items_info['shortDescription']
    # items_result['feature'] = feature

    # print '----------------name--------------'
    title = ''
    if items_info.has_key('name'):
        title = items_info['name']
    items_json['name'] = title

    # print '----------------brand--------------'
    brand = 'no brand'
    if items_info.has_key('brandName'):
        brand = items_info['brandName']
    else:
        brand_info = re.search(r'<span itemprop=brand>(.*?)</span>', items_html, re.S)
        if brand_info != None:
            brand = brand_info.group(1)
    items_json['brand'] = brand

    # print '----------------category--------------'
    category_path = items_info['categoryPath']
    category_string_path = str(category_path).replace('/','>')
    items_json['category'] = category_string_path

    # print '----------------seller_id--------------'
    sellerId = ''
    items_json['seller_id'] = sellerId

    # print '----------------reviews--------------
    reviews = ''
    if items_info.has_key('numReviews'):
        reviews = items_info['numReviews']
    items_json['reviews'] = reviews

    # print '----------------category_id_path--------------'
    category_id_path = items_info['categoryNode']
    category_id_path = str(category_id_path).replace('_','>')
    items_json['category_id_path'] = category_id_path[:-1]

    # print '----------------category_id----------------'
    category_id = category_id_path.split('_')[-1]
    items_json['category_id'] = category_id

    # print '----------------upc--------------'
    items_json['upc'] = items_info['upc']

    # product_attr = ''
    # if items_info.has_key('attributes'):
    #     product_attr = items_info['attributes']
    # items_result['product_attr'] = product_attr

    # print '----------------description-------短描-------'
    feature_list = []
    description_str = ''
    if items_info.has_key('shortDescription'):
        short_description_info = items_info['shortDescription']
        html = HTMLParser.HTMLParser()
        short_description_html = html.unescape(short_description_info)
        short_description = re.sub(r'<[^>]+>', '', short_description_html)
        feature_list = short_description.split('.')

    for description in feature_list:
        description_str = description_str + description + ';'
    items_json['description'] = description_str
    # feature_dic = get_feature_dict(feature_list)

    # print '----------------weight--------------'
    weight_number = 0.0000
    items_json['weight'] = weight_number

    # print '----------------height--------------'
    height_number = 0.0000
    items_json['height'] = height_number

    # print '----------------width--------------'
    width = 0.000
    items_json['width'] = width

    # print '----------------length_class--------------'
    length_class = 'cm'
    items_json['length_class'] = length_class

    # print '----------------weight_class--------------'
    weight_class = 'kg'
    items_json['weight_class'] = weight_class

    # print '----------------url--------------'
    url = items_info['productUrl']
    # url = items_info['url']
    items_json['url'] = str(url)

    # print '----------------detail----------详描----'
    Specifications = {}
    Specifications_list = re.findall(r'<tr class=js-product-specs-row>[\s]*<td>(.*?)</td>[\s]*<td>(.*?)</td>[\s]*</tr>',
                                     items_html, re.S)
    if Specifications_list != []:
        for Specifications_info in Specifications_list:
            tmp1 = re.sub(r'<[^>]+>', '', Specifications_info[0], re.S)
            tmp2 = re.sub(r'<[^>]+>', '', Specifications_info[1], re.S)
            Specifications[tmp1] = tmp2

    items_json['detail'] = str(Specifications)

    # print '----------------image----------------'
    image = ''
    if items_info.has_key('largeImage'):
        image = items_info['largeImage']
    items_json['image'] = image

    # print '----------------attributes----------------'
    items_json['attributes'][0]['price'] = str(price)
    variation_id = str(items_info['parentItemId'])+'_'+str(items_info['itemId'])
    items_json['attributes'][0]['variation_id'] = str(variation_id)
    items_json['attributes'][0]['image'] = image[0]
    # "attributes": [
    #     {"price": "", "variation_id": "", "dictory": "Ships From", "attributes": {"Ships From": ""}, "image": [],
    #      "quantity": 99}]
    json_file = json.dumps(items_json)
    # items_dic = dict(items_result.items() + feature_dic.items())
    return json_file


def get_result(itemsId, i):
    true = True
    null = None
    false = False
    key_list = ['asfas', '', 'z2pqv4dtuwhxe3hkesx9kqpv', 'fmwnnrwf53d6c5sw7b4pu2q3', 'jqpyjz92jmaruene4mpbe8pc',
                'nz2gzu5byp9dbnm6jee69jkp', 'sfpw74s5yte8dj9r9atzyc5m', '2tk5sghn56mnth5uabspkdt6',
                'favxs8n4kvmrtebrn6uymjdy', 'vffn6p33smtby3tytugp8zjt',
                'ctztjz3gfm273husdu7apwwh', 'fwx3gf2qdqhx782h9espqajz', 'f7fqv4jzcdr7ccfb2b339cv9',
                '7sd4rpjfmdurwuwzgvpbffd2']
    key = key_list[i]
    items_url = 'http://api.walmartlabs.com/v1/items/' + str(itemsId) + '?apiKey=' + key + '&format=json'
    print (items_url)
    info = get_html.get_html(items_url)
    items_info = eval(info)
    return items_info


def get_result_list(itemsId):
    try:
        i = 0
        while True:

            try:
                items_info = get_result(itemsId, i)
                # print '----------------------------------------'
                print (items_info)
                break
            except Exception as e:
                if str(e) == 'time out':
                    pass
                else:
                    i += 1
                    if i > 14:
                        spct_file.write(itemsId + '\n')
                        spct_file.flush()
                        break
        i = i
        print (i)
        items_list_info = []
        if items_info.has_key('variants'):
            items_id_list = items_info['variants']
            for items_id in items_id_list:
                while True:

                    try:
                        items_info = get_result(itemsId, i)
                        # print '----------------------------------------'
                        # print items_info
                        break
                    except Exception as e:
                        if str(e) == 'time out':
                            pass
                        else:
                            i += 1
                            if i > 14:
                                break

                items_result = get_info(items_info)
                items_list_info.append(items_result)
        else:
            items_result = get_info(items_info)
            items_list_info.append(items_result)
        return items_list_info
    except Exception as e:
        print (e)


def handle(items_id):
    try:
        print ('...')
        itemsId = str(items_id).replace('\n', '')
        items_list_info = get_result_list(itemsId)
        for items_info in items_list_info:
            print (items_info)

            # for k in titles:
            #     if items_info.has_key(k):
            #         value = items_info.get(k)
            #     else:
            #         value = 'None'
            #     lock.acquire()
            #     result_file.write(str(value) + "\t")
            #     result_file.flush()
            #     lock.release()

            lock.acquire()
            result_file.write(items_info+'\n')
            result_file.flush()
            lock.release()
    except Exception as e:
        print (e)


def get_items(id_file):
    global false, true, null
    global spct_file, items_file, result_file
    global lock, titles
    lock = Lock()

    result_file = open('./result/DB/items_db.csv', 'aw')
    items_file = open(id_file, 'r')
    spct_file = open('./result/DB/spct.txt', 'w')
    id_list = items_file.readlines()
    pool = Pool(1)
    pool.map(handle, id_list)
    pool.close()
    pool.join()
    spct_file.close()
    result_file.close()
    items_file.close()


if __name__ == "__main__":
    get_items('./result/DB/itemsId_db_last.txt')
