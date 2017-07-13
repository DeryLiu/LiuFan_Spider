from multiprocessing import Lock, Pool

import time
from Tools import get_html
import re

def get_info(html):
    # html = get_html.get_html_src(url)
    # print html
    items_info_list = []
    # print '--------------itemsId---------------'
    try:
        itemsId = re.findall(r'<span class="fs16 c28" data-selenium="bhSku">(.*?)</span>',html,re.S)
        itemsId = str(itemsId).split('B&H&nbsp;#&nbsp;')[1]
        itemsId = str(itemsId).split('\\n\\t')[0]
    except Exception as e:
        itemsId = e
    items_info_list.append(itemsId)
    # print itemsId

    # print '--------------price-----------------'
    try:
        price = re.findall(r'<meta itemprop="price" content="(.*?)" />',html,re.S)
        price = ''.join(price)
    except Exception as e:
        price = e
    items_info_list.append(price)
    # print price

    # print '---------------ship-----------------'
    # ship = re.findall(r'')
    ship = 'None'
    items_info_list.append(ship)

    # print '---------------stock----------------'
    try:
        stock = re.findall(r'<span class="c29 fs16 bold upper" data-selenium="inStock">(.*?)</span>',html,re.S)
        stock = ''.join(stock)
    except Exception as e:
        stock = e
    items_info_list.append(stock)
    # print stock

    # print '---------------brand----------------'
    try:
        brand = re.findall(r'<span itemprop="brand">(.*?)</span>',html,re.S)
        brand = ''.join(brand)
    except Exception as e:
        brand = e
    items_info_list.append(brand)
    # print brand

    # print '--------------title-----------------'
    try:
        title = re.findall(r'<span itemprop="name">(.*?)</span>',html,re.S)
        title = str(title).replace('\\t','').replace('\\n','')
        name = title.split("'")[1]
        # title = ''.join(title)
        t_name = brand+' '+name
    except Exception as e:
        t_name = e
    items_info_list.append(t_name)
    # print title

    # print '--------------image-----------------'
    # <a class="noUnderline clearfix enlargeMain" name="enlarge" href="https://www.bhphotovideo.com/images/images2500x2500/asus_c202sa_ys02_11_6_c202sa_series_16_1254167.jpg" data-cmelemtag="{&quot;elemId&quot;:&quot;ASC202YS02DB-REG&quot;,&quot;elemCat&quot;:&quot;MAIN:Image`Zoom`Dtl&quot;}" data-selenium="enlargeMain" itemprop="image">

    try:
        image_list = []
        image_list_re = re.findall(r'<a class="noUnderline clearfix enlargeMain" name="enlarge" href="(.*?)"',html,re.S)
        image_list.extend(image_list_re)
        image_last = str(image_list_re).split('_')[-1]
        image_url_string_list = str(image_list_re).split('_')[:-1]
        image_url_string = 'https://www.bhphotovideo.com/images/images2500x2500/apple'
        for imageurl in image_url_string_list[1:]:
            image_url_string = image_url_string+ '_'+ imageurl
        # image_url_string = image_url_string+'_'
        # print 'image_url_string'+str(image_url_string)
        image_last_num = float(image_last.split('.')[0])
        # print 'image_last_num'+ str(image_last_num)
        for i in range(1,3):
            image_num = image_last_num+i
            image_url = str(image_url_string)+'_'+str(image_num)+'.jpg'
            # print 'image_url'+str(image_url)
            image_list.append(image_url)

        # try:
        #     image_list1 = re.findall(r'data-src="(.*?)"',str(image_list_re),re.S)
        # except:
        #     image_list1 = [' ',' ',' ']
        # image_list = [str(ima).split('"')[0] for ima in image_list1]
        # while len(image_list)<3:
        #     image_list.append(' ')
    except Exception as e:
        print (e)
    items_info_list.extend(image_list)
    # print image_list2

    # print '--------------detail-----------------'
    try:
        detail_list_re = re.findall(r'<ul class="top-section-list" data-selenium="highlightList">(.*?)</ul>',html,re.S)
        # print detail_list_re
        detail_list = re.findall(r'<li class="top-section-list-item">(.*?)</li>',str(detail_list_re),re.S)
        # print detail_list

        if len(detail_list)>6:
            detail_list = detail_list[:5]
        # elif len(detail_list)<4:
        #     detail_list = detail_list.append('')
    except Exception as e:
        detail_list = [' ',' ',' ',' ',' ']
        print (html)
    items_info_list.extend(detail_list)
    # print detail_list

    # print '-------------Specification------------'
    specification = ''
    items_info_list.append(specification)
    # print specification

    print ('---------------end--------------------')
    print (items_info_list)
    # lock.acquire()
    # items_info.write('\t'.join(items_info_list)+'\n')
    items_info.write('\t'.join(str(v) for v in items_info_list)+'\n')
    # items_info.flush()
    # lock.release()

def get_items_html(items_file):
    global lock,pool,items_info
    title_list = ['itemsId', 'price', 'ship', 'stock', 'brand', 'title', 'img1', 'img2', 'img3', 'detail1', 'detail2', 'detail3', 'detail4', 'detail5','Specification']
    file_name = './Hidden Cameras.xls'
    items_info = open(file_name, 'aw')
    items_info.write('\t'.join(title_list) + '\n')
    items_info.flush()

    items_list = open(items_file,'r').readlines()

    for it in items_list:
        print (it)
        html = get_html.get_html(it)
        # time.sleep(2.5)
        get_info(html)

    items_info.close()

if __name__ == '__main__':
    items_url_file = './items_url.txt'
    get_items_html(items_url_file)