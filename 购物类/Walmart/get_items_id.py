from multiprocessing import Pool
import os
import re
import requests
from Tools import get_html

def handle(list_url):
    try:
        url_info = list_url.split("\t")
        url = url_info[-1].replace("\n", "")
        list_num = url_info[0]
        #     http://www.walmart.com/browse/books/top-200-books/1229749_1044270?page=2&cat_id=1229749_1044270&facet=retailer:Walmart.com&min_price=0&max_price=5
        items_url_info = url.split("?")
        if int(list_num) > 1000:
            list_num = 1000
        if int(list_num) % 40 > 0:
            page_num = int(list_num) / 40 + 1
        else:
            page_num = int(list_num) / 40
        for page in range(1, page_num + 1):
            items_url = items_url_info[0] + '?page=' + str(page) + '&' + items_url_info[1]
            html = get_html.get_html(items_url)
            itemsId_info = re.search(r'"displayOrder":\[(.*?)\]', html, re.S)
            itemsId_all = itemsId_info.group(1).replace('"', '')
            items_list = itemsId_all.split(',')
            for itemsId in items_list:
                result_file.write(itemsId + '\n')
                result_file.flush()
                print (itemsId)
    except Exception as e:
        print (e)
        pass


def get_list(list_file):
    global result_file
    result_file = open('./result/itemsId.txt', 'w')
    list_url_file = open(list_file, 'r')
    list_url_list = list_url_file.readlines()
    pool = Pool(8)
    pool.map(handle, list_url_list)
    pool.close()
    pool.join()
    list_url_file.close()
    result_file.close()


if __name__ == "__main__":
    get_list('./result/list.txt')
    os.system('sort -u ' + './result/itemsId.txt' + ' > ' + './result/itemsId_last.txt')