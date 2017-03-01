import codecs
from multiprocessing import Pool, Lock
import re
import time
from selenium import webdriver
from Tools import get_html

#把list洗乱
def shuffle_list(list_name):

    from random import shuffle
    shuffle(list_name)
    # 返回随机排序后的序列
    return list_name

#获取描述
def get_feature_dict(detail):

    feature = ['detail1', 'detail2', 'detail3', 'detail4', 'detail5']
    feature_len = len(feature)
    features = detail
    feature_count = len(features)
    if feature_count < feature_len:
        features += ['' for _i in range(feature_len - feature_count)]
    feature_dict = dict(zip(feature, features))
    return feature_dict

#获取图片
def get_img_dict(image):

    img_list = ['img1', 'img2', 'img3', 'img4', 'img5']
    img_list_len = len(img_list)
    imgs = image[:5]  # 最多取8张图片
    while '' in imgs:
        imgs.remove('')
    img_count = len(imgs)
    if img_count > 2:
        t_imgs = imgs[:1]
        t_imgs.extend(shuffle_list(imgs[1:]))
        imgs = t_imgs
    if img_count < img_list_len:
        imgs += ['' for _i in range(img_list_len - img_count)]
    img_dict = dict(zip(img_list, imgs))
    return img_dict

#传入商品页面的html和商品的id
def get_info(html, itemsId):
    items_info = {'itemsId': itemsId, 'price': '', 'Original_price': '', 'ship': '', 'stock': '', 'brand': '',
                  'title': '', 'Specification': ''}
    #读取价格字段存入
    # print '---------------------price----------------------'
    price = re.findall("<meta itemprop='price' content='(.*?)'", html)[0]
    # print price
    items_info['price'] = price

    #售价页
    # print '---------------------Original_price----------------------'
    url = 'http://www.newegg.com/Product/MappingPrice2012.aspx?Item=' + itemsId+'&recaptcha=pass'
    html_price = get_html.get_html_requests(url)
    orgin_price = re.findall('<span class="price-was-data" style="display: none">(.*?)</span>', html_price)
    if orgin_price:
        orgin_price = orgin_price[0]
    else:
        orgin_price = 'None'

    items_info['Original_price'] = orgin_price

    # print '---------------------ship----------------------'
    ship = '0'
    ship = re.search(r'product_default_shipping_cost:\[(.*?)\]', html)
    if ship:
        ship = ship.group(1).replace("'", "")
    items_info['ship'] = ship

    # print '---------------------stock----------------------'
    stock = ''
    stock_info = re.search(r'product_instock:\[(.*?)\]', html)
    if stock_info:
        stock_info = stock_info.group(1).replace("'", "")
        if int(stock_info) == 1:
            stock = 'In stock'
        else:
            stock = 'out of stock'
    items_info['stock'] = stock

    # print '---------------------brand----------------------'
    brand = ''
    brand = re.search(r'product_manufacture:\[(.*?)\]', html)
    if brand:
        brand = brand.group(1).replace("'", "")
    items_info['brand'] = brand

    # print '---------------------name----------------------'
    name = ''
    name_info = re.search(r'product_title:\[(.*?)\]', html)
    if name_info:
        name = name_info.group(1).replace("'", "").replace('&amp;', '').replace("#34;", "''").replace("#40;",
                                                                                                      "(").replace(
            '#41;', ')').replace("#47;", "\\")
        name = name.decode("ascii").encode("utf-8")
    items_info['title'] = name

    # print '---------------------Specification----------------------'
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
    items_info['Specification'] = str(Specification).replace('{', '').replace('}', '').replace("'", '').replace(',',
                                                                                                                '<br>')
    if len(items_info['Specification']) >= 1000:
        items_info['Specification'] = items_info['Specification'][0:999]

    # print '---------------------image----------------------'
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
    image_dict = get_img_dict(image)

    # print '---------------------details----------------------'
    details = []
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
    detail_dict = get_feature_dict(details)
    items_dict = dict(items_info.items() + image_dict.items() + detail_dict.items())  # 所有字典合并
    for k in titles:
        if items_dict.has_key(k):
            value = items_dict.get(k)
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

#把itemsId页面的html传入get_info函数中，把失败的id重新存一个文件
def handle(itemsId):
    # 删除itemsId开头结尾处的空格
    itemsId = itemsId.strip()
    # 商品详情页
    url = 'http://www.newegg.com/Product/Product.aspx?Item=' + itemsId
    # 获取每一个商品页面的html
    # time.sleep(5)
    try:
        html = get_html.get_html_requests(url)

        if html:
            #调用get_info函数，传入html和每个商品的id
            get_info(html, itemsId)
            # driver.quit()
        else:
            with open('./get_html_fail.txt', 'aw') as h:
                h.write(itemsId + '\n')
            # driver.close()

    except Exception as e:
        print (url)
        print (itemsId, ":",  e)
        with open('./except.txt', 'aw') as f:
            f.write(itemsId + '\n')
        # driver.close()

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

    global result_file, lock, titles

    titles = ['itemsId', 'price', 'Original_price', 'ship', 'stock', 'brand', 'title', 'img1', 'img2', 'img3', 'img4',
              'img5', 'detail1', 'detail2', 'detail3', 'detail4', 'detail5', 'detail6',
              'feature', 'Specification']
    item_file = open(items_file, 'r')

    result_file_name = './UPS Accessories.xls' #
    #调用函数create_titles
    create_titles(result_file_name, titles)
    result_file = open(result_file_name, 'aw')
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
    start('./items_last.txt')
