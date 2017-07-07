# # -*- coding: gbk -*-
# import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.action_chains import ActionChains
# from multiprocessing import Pool,Lock
# from selenium import webdriver
#
# driver = webdriver.Chrome(executable_path='/Users/Dery/SeleniumWebDriver/chromedriver')
# # driver = webdriver.PhantomJS(executable_path='/Users/Dery/SeleniumWebDriver/phantomjs-2.1.1-macosx/bin/phantomjs')
# # driver.set_window_size('2000','800')
# driver.get('http://www.kujiale.com/signin')
# driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div/div[2]/div[1]/div[1]/ul/li[2]/a').click()
# driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/form/ul/li[1]/div/label/input').clear()
# driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/form/ul/li[1]/div/label/input').send_keys('15867869636')
# driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/form/ul/li[2]/div/label/input').clear()
# driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/form/ul/li[2]/div/label/input').send_keys('asd123#')
# # 登陆
# driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/div/a').click()
# # 开始设计
# time.sleep(3)
# ActionChains(driver).move_to_element_with_offset('',200,200).click()
# driver.get('http://www.kujiale.com/huxing/flash')
# time.sleep(90)
# # 搜索户型图
# driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/ul/li[2]/a').click()
# # 搜索
# driver.find_element_by_css_selector('body > div.search-results > div.results-wrapper > div > div > div > div.search-form.clearfix > div.search.fl > a').click()
# # driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div[1]/div[2]/a').click()
# for page in range(15):
#     driver.find_element_by_css_selector('div.hx-list > div:nth-of-type({})'.format(page+1)).click()
#     driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/div[3]/div/a[1]').click()
#     time.sleep(10)
#     # 完成
#     ActionChains(driver).move_to_element_with_offset('',3800,80).click()
#     driver.get('http://www.kujiale.com/huxing/flash')
#     driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/ul/li[2]/a').click() # 搜索户型图
#     driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/div/div/div[1]/div[2]/a').click()
#
# driver.quit()
#
sss =  open('text.html','r')
with open('text.csv','w') as aaaa:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(sss.read(),'html.parser')
    city_name = '上海'
    name_list = soup.select('#content > div.detail > div.list-bd > ul > li > div > p > a')
    img_list = soup.select('#content > div.detail > div.list-bd > ul > li > a > img')
    # print(len(name_list))
    # print(len(img_list))
    try:
        for i in range(9):
            print(name_list[i].text.split('_')[1])
            print(img_list[i]['data-url'])
            aaaa.write(city_name+'\t'+name_list[i].text.split('_')[1]+'\t'+img_list[i]['data-url'].split('@')[0]+'\n')
    except:
        pass
