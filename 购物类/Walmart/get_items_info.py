import HTMLParser
from multiprocessing import Pool, Lock
import re
import sys  # 引用sys模块进来，并不是进行sys的第一次加载
import requests
import reload

reload(sys)  # 重新加载sys
sys.setdefaultencoding('utf8')
from Tools import get_html


def get_feature_dict(detail):  # 将列表形式特征字段转换成字典形式


    feature = ['detail1', 'detail2', 'detail3', 'detail4', 'detail5']
    feature_len = len(feature)
    features = detail
    feature_count = len(features)
    if feature_count < feature_len:
        features += ['' for _i in range(feature_len - feature_count)]
    feature_dict = dict(zip(feature, features))
    return feature_dict


def get_info(items_info):  # 得到字段信息
    # items_result={'itemsId':'','price':'','ship':'','stock':'','image1':'','brand':'','title':'','product_attr':'','description':'','Specification':''}
    items_result = {'itemsId': '', 'price': '', 'ship': '', 'stock': '', 'image1': '', 'brand': '', 'title': '',
                    'product_attr': '', 'Specification': ''}
    price = ''
    if items_info.has_key('salePrice'):
        price = items_info['salePrice']
    items_result['price'] = price

    sku = ''
    if items_info.has_key('itemId'):
        sku = items_info['itemId']
    items_result['itemsId'] = sku
    items_url = 'http://www.walmart.com/ip/' + str(sku)
    item_html = ''
    try:
        items_html = get_html.get_html(items_url)
    except Exception as e:
        print (e)

    stock = ''
    if items_info.has_key('stock'):
        stock_info = items_info['stock']
        if stock_info == 'Not Available' or stock_info == 'Not available':
            stock = 'out of stock'
        if stock_info == 'Available':
            stock = 'in stock'
    items_result['stock'] = stock

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

    ship = '0'
    if items_info.has_key('standardShipRate'):
        ship = items_info['standardShipRate']
    items_result['ship'] = ship

    feature = ''
    if items_info.has_key('shortDescription'):
        feature = items_info['shortDescription']
    items_result['feature'] = feature

    title = ''
    if items_info.has_key('name'):
        title = items_info['name']
    items_result['title'] = title

    brand = ''
    if items_info.has_key('brandName'):
        brand = items_info['brandName']
    else:
        brand_info = re.search(r'<span itemprop=brand>(.*?)</span>', items_html, re.S)
        if brand_info != None:
            brand = brand_info.group(1)

    items_result['brand'] = brand

    reviews = ''
    if items_info.has_key('numReviews'):
        reviews = items_info['numReviews']
    items_result['reviews'] = reviews

    product_attr = ''

    if items_info.has_key('attributes'):
        product_attr = items_info['attributes']
    items_result['product_attr'] = product_attr

    feature_list = []
    if items_info.has_key('shortDescription'):
        short_description_info = items_info['shortDescription']
        html = HTMLParser.HTMLParser()
        short_description_html = html.unescape(short_description_info)
        short_description = re.sub(r'<[^>]+>', '', short_description_html)
        feature_list = short_description.split('.')
    feature_dic = get_feature_dict(feature_list)

    Specifications = {}
    Specifications_list = re.findall(r'<tr class=js-product-specs-row>[\s]*<td>(.*?)</td>[\s]*<td>(.*?)</td>[\s]*</tr>',
                                     items_html, re.S)
    if Specifications_list != []:
        for Specifications_info in Specifications_list:
            tmp1 = re.sub(r'<[^>]+>', '', Specifications_info[0], re.S)
            tmp2 = re.sub(r'<[^>]+>', '', Specifications_info[1], re.S)
            Specifications[tmp1] = tmp2
        if len(str(Specifications)) > 1000:
            Specifications = str(Specifications)[:1000]
    items_result['Specification'] = Specifications

    if items_info.has_key('largeImage'):
        image = items_info['largeImage']
    items_result['img1'] = image

    items_dic = dict(items_result.items() + feature_dic.items())
    return items_dic


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
                print ('----------------------------------------')
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
                        print ('----------------------------------------')
                        print (items_info)
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
            for k in titles:
                if items_info.has_key(k):
                    value = items_info.get(k)
                else:
                    value = 'None'
                lock.acquire()
                result_file.write(str(value) + "\t")
                result_file.flush()
                lock.release()

            lock.acquire()
            result_file.write('\n')
            result_file.flush()
            lock.release()
    except Exception as e:
        print (e)


def create_titles(filename, titles):
    f = open(filename, "w")
    f.write("\t".join(titles) + "\n")
    f.flush()
    f.close()


def get_items(id_file):
    global false, true, null
    global spct_file, items_file, result_file
    global lock, titles
    lock = Lock()
    # titles=['itemsId','price','ship','stock','brand','title','product_attr','img1','img2','img3','img4','img5','img6','img7','img8','detail1','detail2','detail3','detail4','detail5','detail6','description','Specification']
    titles = ['itemsId', 'price', 'ship', 'stock', 'brand', 'title', 'product_attr', 'img1', 'img2', 'img3', 'img4',
              'img5', 'img6', 'img7', 'img8', 'detail1', 'detail2', 'detail3', 'detail4', 'detail5', 'detail6',
              'Specification']

    result_file_name = './result/Soccer Shinguards.xls'

    create_titles(result_file_name, titles)
    result_file = open(result_file_name, 'aw')
    items_file = open(id_file, 'r')
    spct_file = open('./result/spct.txt', 'w')
    id_list = items_file.readlines()
    pool = Pool(1)
    pool.map(handle, id_list)
    pool.close()
    pool.join()
    spct_file.close()
    result_file.close()
    items_file.close()


if __name__ == "__main__":
    get_items('./result/itemsId_last.txt')
