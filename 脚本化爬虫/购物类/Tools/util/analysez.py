import urllib2
import re
import os
from multiprocessing import Pool, Lock


'''
Home > Books > Antiques & Collectibles > Art
81 - 1580
'''

def get_isbn(urls):
    '''<a href="http://product.half.ebay.com/Handbooks-in-International-Art-Business-Art-Collection-Management-a-Handbook-for-Collectors-and-Art-Professionals-by-Mary-Rozell-2014-E-book/208707357&amp;tg=info" class="pdplinks">1848221428</a>'''
    isbn_info = open('./result/isbn_info','aw')

    isbn_list = re.findall(r'<a href="'+ urls +'" class="pdplinks">(.*?)</a>',urls,re.S)
    isbn_dict = {'isbn_10':'','isbn_13':''}
    for isbn in isbn_list:
        isbn_10 = isbn[0]
        isbn_13 = isbn[1]
        isbn_dict['isbn_10'] = isbn_10
        isbn_dict['isbn_13'] = isbn_13

    isbn_info.write(urls+'\t'+isbn_dict+'\n')
    isbn_info.flush()
    isbn_info.close()

def get_items_url():
    base_url = 'http://books.products.half.ebay.com/Art-Antiques-Collectibles_W0QQ_trksidZp3032QQpgZ[i]QQcZ4QQcatZ218230'

    for i in range(1, 82):
        url = base_url.replace("[i]", str(i))
        print url

        html = urllib2.urlopen(urllib2.Request(base_url)).read()

        main_pages = re.findall(r'<div style="float:left;" itemscope="itemscope" itemtype="http://schema.org/SearchResultsPage">.*?<a href="(.*?)">',html,re.S)

        print '=========='
        detail_url = []
        for items_url in main_pages:
            with open("./id.txt", "aw") as f:
                f.write(items_url + "\n")
                print items_url
                detail_url.append(items_url)

        pool = Pool(5)
        pool.map(get_isbn, detail_url)
        pool.close()
        pool.join()

    # os.system('sort -u ' + './items.txt' + ' > ' + './items_last.txt')

