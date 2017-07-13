import re
from Tools import get_html
import os
#page_num 为此品类页码数
#base_url 为要抓取的品类页面
#遍历所有页面，获取每个页面的html，保存到html文件中，命名为页数
def get_all_url(page_num, base_url):

    for i in range(1, page_num+1):
        url = base_url
        url += str(i)
        print (url)
        html = get_html.get_html(url)
        if html:
            ff = open('./html/' + str(i), 'w')
            ff.write(html)
            print ('write html succeed')
        else:
            print ('write html error')

#
def get_items():

    result_file = open('./items.txt', 'w')
    #在保存的html文件里遍历
    for i in os.listdir('./html'):
        html = open('./html/' + str(i), 'r').read()

        #<input id="CompareItem_9SIA97A4TG0647" autocomplete="off" neg-itemnumber="9SIA97A4TG0647" type="checkbox"
        # name="CompareItem" value="CompareItem_9SIA97A4TG0647">
        #取后面的字符串，以列表形式保存
        items = re.findall(r'value="CompareItem_(.*?)"', html)
        print (len(items))
        for item in items:
            #items.txt里保存的是截取的字段
            result_file.write(item + '\n')


if __name__ == '__main__':
    #当前品类只有30页
    # get_all_url(page_num=30, base_url='http://www.newegg.com/Product/ProductList.aspx?Submit=ENE&N=100008241%204814%204017%204018%204019%204020%204023%204026%204027%204084%204092&IsNodeId=1&bop=And&PageSize=60&order=BESTMATCH&Page=')
    url = '''http://www.newegg.com/Product/ProductList.aspx?Submit=ENE&N=100014346%208000%204814&IsNodeId=1&bop=And&ActiveSearchResult=True&order=BESTMATCH&Page='''
    get_all_url(page_num=10,base_url=url)
    get_items()
    #去重
    os.system('sort ./items.txt|uniq > ./items_last.txt')