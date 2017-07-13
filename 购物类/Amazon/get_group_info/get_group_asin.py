import time
import random
import os
from Tools import get_html,ALL_CONFIG
from multiprocessing import Pool, Lock
import re

def get_asin():
    #Electronics : Computers & Accessories : Monitors : Prime Eligible : New

    base_url = '''https://www.amazon.com/s/ref=sr_pg_[i]?fst=as%3Aoff&rh=n%3A172282%2Cn%3A!493964%2Cn%3A172541%2Cn%3A12097478011%2Cp_85%3A2470955011%2Cp_n_condition-type%3A2224371011&page=[i]&bbn=12097478011&ie=UTF8&qid=1479085629'''

    for i in range(1, 222):  # 页码，共2页
        url = base_url.replace("[i]", str(i))
        print (url)
        time.sleep(2)
        html = get_html.get_html(url)

        url_list = re.findall(r'<a class="a-link-normal s-access-detail-page .*? href="(.*?)">', html, re.S)
        print (len(url_list))

        for goods_url in url_list:
            with open(ALL_CONFIG.AMAZON_GROUP_URL_FILE, "aw") as f:
                f.write(goods_url + "\n")
                print (goods_url)
            items_asin = re.findall(r'/dp/(.*?)/ref',goods_url,re.S)
            # for item_asin in items_asin:
            #     with open("./Result/items_asin.txt",'aw') as asin:
            #         asin.write(item_asin+'\n')
            #         print item_asin


if __name__ == "__main__":
    get_asin()
