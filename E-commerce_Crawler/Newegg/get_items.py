import os
import re
from Tools import get_html,ALL_CONFIG

def except_new():
    all_file = open('./items_all.txt','r')
    new_file = open('./items_new.txt','r')
    last_file = open('./items.txt','aw')
    all_list = []
    new_list = []
    for all_item in all_file.readlines():
        all_item = all_item.split('\n')[0]
        all_list.append(all_item)
    print (len(all_list))

    for new_item in new_file.readlines():
        new_item = new_item.split('\n')[0]
        new_list.append(new_item)
    print (len(new_list))

    final_list = list(set(all_list+new_list))
    print (len(final_list))
    for fin in final_list:
        last_file.write(fin+'\n')

def get_newegg_url(page_num,new_url):
    for i in range(1, page_num + 1):
        url = new_url
        url += str(i)
        print (url)
        html = get_html.get_html(url)

        result_file = open('./items_new.txt', 'aw')
        if html:
            # <input id="CompareItem_9SIA97A4TG0647" autocomplete="off" neg-itemnumber="9SIA97A4TG0647" type="checkbox"
            # name="CompareItem" value="CompareItem_9SIA97A4TG0647">
            # 取后面的字符串，以列表形式保存
            items = re.findall(r'value="CompareItem_(.*?)"', html)
            print (len(items))
            for item in items:
                # items.txt里保存的是截取的字段
                result_file.write(item + '\n')
        else:
            print ('write html error')

#page_num 为此品类页码数
#base_url 为要抓取的品类页面
#遍历所有页面，获取每个页面的html，保存到html文件中，命名为页数
def get_all_url(page_num, base_url):

    for i in range(1, page_num+1):
        url = base_url
        url += str(i)
        print (url)
        html = get_html.get_html_requests(url)
        # print html

        result_file = open('./items_all.txt', 'aw')
        if html:
            # <input id="CompareItem_9SIA97A4TG0647" autocomplete="off" neg-itemnumber="9SIA97A4TG0647" type="checkbox"
            # name="CompareItem" value="CompareItem_9SIA97A4TG0647">
            # 取后面的字符串，以列表形式保存
            items = re.findall(r'value="CompareItem_(.*?)"', html)
            print (len(items))
            for item in items:
                # items.txt里保存的是截取的字段
                result_file.write(item + '\n')
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
    pan = input('除newegg？\n')

    all_url = 'http://www.newegg.com/Product/ProductList.aspx?Submit=ENE&N=100008042%204814&IsNodeId=1&bop=And&Page='
    all_page = 100
    new_url = 'http://www.newegg.com/Product/ProductList.aspx?Submit=ENE&N=100006740%204814%208000&IsNodeId=1&bop=And&order=BESTMATCH&page=1'
    new_page = 0

    if pan =='y':
        get_all_url(page_num=all_page,base_url=all_url)
        get_newegg_url(page_num=new_page,new_url=new_url)
        # get_items()
        except_new()
    else:
        get_all_url(page_num=all_page,base_url=all_url)

    #去重
    os.system('sort ./items_all.txt|uniq > ./items_last.txt')