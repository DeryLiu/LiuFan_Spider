import json
from Tools import ALL_CONFIG
from selenium import webdriver
import re

#把itemsId页面的html传入get_info函数中，把失败的id重新存一个文件
def start():
    try:
        driver = webdriver.PhantomJS(executable_path=ALL_CONFIG.PHANTOMJS_PATH)

        items_list = open(ALL_CONFIG.AMAZON_GROUP_ITEMS_FILE, 'r').readlines()
        for item in items_list:
            item = item.split('\n')[0]

            driver.get(item)

            itemsId_list = re.findall(r'/dp/(.*?)/ref', item, re.S)
            sign = ''.join(itemsId_list)
            sign = str(sign)

            html = driver.page_source  # 这就是返回的页面内容了
            group_list_html = re.findall(r'<ul class="a-nostyle a-horizontal a-spacing-base a-spacing-top-base sims-fbt-image-box">(.*?)</ul>',html, re.S)
            group_url_list = re.findall(r'href="(.*?)"', str(group_list_html), re.S)

            first = sign+'>'+item
            group_url = [first]
            for url_part in group_url_list:
                url_part = sign+'>'+'http://www.amazon.com' + url_part
                group_url.append(url_part)

            # group_dict= {'sign':sign,'itemsURL':group_url}

            print ('=-=-=-=-=-=')
            print (group_url)

            # with open('./Result/Group/items_group_url.csv', 'aw') as result_file:
            #     result_file.write(json.dumps(group_dict)+'\n')
            for items_url in group_url:
                with open('./Result/Group/items_group_url.csv', 'aw') as result_file:
                    result_file.write(items_url+'\n')
        driver.quit()
    except Exception as e:
        print (e)


if __name__ == "__main__":
    start()
