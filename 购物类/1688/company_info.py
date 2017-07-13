from multiprocessing import Lock, Pool
from selenium.webdriver import ActionChains
import re
import json
import time
from selenium import webdriver
from PIL import Image,ImageEnhance
from Tools import ALL_CONFIG
def create_titles(filename, titles):
    f = open(filename, "w")
    f.write("\t".join(titles) + "\n")
    #清除内部缓冲区
    f.flush()
    #关闭文件
    f.close()
#
# def get_product_url(info):
#     time.sleep(5.5)
#     try:
#         info_url = 'http'+info.split('http')[1]
#         basic_info = info.split('http')[0]
#         driver.get(info_url)
#         html = driver.page_source
#         product_page = re.findall(r'<li class=" " data-page-name="creditdetail">(.*?)</li>',html,re.S)
#         product_url = str(product_page).split('href="')[1]
#         product_url = product_url.split('"')[0]
#         print product_url
#         return product_url
#     except:
#         pass

def get_credit_record(info):
    time.sleep(8)
    try:
        info_url = 'http'+info.split('http')[1]
        basic_info = info.split('http')[0]

        time.sleep(5)
        driver.implicitly_wait(30)
        # req = urllib2.Request(info_url, headers=headers)
        # response = urllib2.urlopen(req,timeout=10)
        # product_html = response.read()
        #------
        driver.get(info_url)
        driver.implicitly_wait(60)
        product_html = driver.page_source

        # product_html = get_html.get_html(info_url)
        print (info_url)
        print (driver.current_url)
        # yanzhengma
        driver.get_screenshot_as_file('./Image/'+basic_info+'.jpg')

        # im = Image.open('./Image/'+basic_info+'.jpg')
        # box = (516, 417, 564, 437)  # 设置要裁剪的区域
        # region = im.crop(box)  # 此时，region是一个新的图像对象。
        # region.show()#显示的话就会被占用，所以要注释掉
        # region.save("./Image/code.jpg")
        # SecretCode = raw_input('please enter the code: ')

        # print product_html
        credit_record = re.findall(r'<div class="section-main" id="J_CompanyTradeCreditRecord">(.*?)</div>',product_html,re.S)
        # print credit_record
        finally_list = []
        finally_list.append(basic_info)
        # self_num_list = []
        temp_llist = []

        self_num_list_2 = re.findall(r'<p class="record-num ">(.*?)</p>',str(credit_record),re.S)
        # print self_num_list_2
        temp_llist.extend(self_num_list_2)

        self_num_list_3 = re.findall(r'<p class="record-num">(.*?)</p>',str(credit_record),re.S)
        self_num_list_3 = str(self_num_list_3).split('<')[0]
        self_num_list_3 = self_num_list_3.split("['")[1]
        # print self_num_list_3
        temp_llist.append(self_num_list_3)

        self_num_list_6 = re.findall(r'<p class="record-num rise">(.*?)</p>',str(credit_record),re.S)
        for num6 in self_num_list_6:
            num6 = str(num6).split('<')[0]
            temp_llist.append(num6)
        # self_num_list.extend(self_num_list_6)
        # finally_list.extend(self_num_list)

        compare_num_list = re.findall(r'<p class="record-contrast-num">(.*?)</p>',str(credit_record),re.S)
        for cmun in compare_num_list:
            cmun = str(cmun).split('<')[0]
            temp_llist.append(cmun)

        finally_list.extend(temp_llist)

        # print compare_num_list
        # info_dict = {'all_deal_record':self_num_list[0],'all_buyer_num':self_num_list[1],'重复采购率':self_num_list[2],
        #              '近90天退款率':self_num_list[3],'近90天投诉率':self_num_list[4],'近90天纠纷率':self_num_list[5],
        #              '成交数同比行业':compare_num_list[0],'买家数同比行业':compare_num_list[1],'采购率同比行业':compare_num_list[2],
        #              '退款率同比行业':compare_num_list[3],'投诉率同比行业':compare_num_list[4],'纠纷率同比行业':compare_num_list[5]}
        # lock.acquire()
        print ('-=-=-=-=')
        print (finally_list)
        result_file.write("\t".join(finally_list) + "\n")

        # with open('./Company/'+basic_info+'.txt','w') as html_info:
        #     html_info.write(product_html)
        # result_file.flush()
        # lock.release()
        # driver.close()
    except:
        pass

def star(url_list):
    global result_file,lock,pool
    url_file = open(url_list,'r')
    info_items = url_file.readlines()
    # print info_items

    result_file = open('./Resutlt/company_info.txt','aw')
    title = ['id1','id2','name','成交数', '买家数', '重复采购率', '近90天退款率', '近90天投诉率', '近90天纠纷率', '成交数同比行业',
             '买家数同比行业', '采购率同比data_行业', '退款率同比行业', '投诉率同比行业', '纠纷率同比行业']
    create_titles('./Resutlt/company_info.txt',title)

    # print info_items
    for info in info_items:
        time.sleep(3)
        get_credit_record(info)

    # lock = Lock()
    # pool = Pool(5)
    # # 调用函数把items_list的内容依次传入handle函数中
    # pool.map(get_credit_record, info_items)
    # pool.close()
    # pool.join()

    url_file.close()
    result_file.close()

def signTaoBao():
    # 匿名爬虫
    # 假定9999端口开启tor服务
    global driver,headers
    service_args = ['--proxy=localhost:9999', '--proxy-type=socks5', ]

    driver = webdriver.PhantomJS(executable_path=ALL_CONFIG.PHANTOMJS_PATH)
    # driver.maximize_window()

    driver.get('https://login.taobao.com/member/login.jhtml?style=mini&amp;css_style=b2b&amp;from=b2b&amp;full_redirect=true&amp;redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253Dhttp%25253A%25252F%25252Flogin.1688.com%25252Fmember%25252FtaobaoSellerLoginDispatch.htm&amp;reg=http%3A%2F%2Fmember.1688.com%2Fmember%2Fjoin%2Fenterprise_join.htm%3Flead%3Dhttp%253A%252F%252Flogin.1688.com%252Fmember%252FtaobaoSellerLoginDispatch.htm%26leadUrl%3Dhttp%253A%252F%252Flogin.1688.com%252Fmember%252FtaobaoSellerLoginDispatch.htm%26tracelog%3Dlogin_s_reg')
    # login TaoBaomn
    # driver.find_element_by_id("J_Static2Quick").click()
    time.sleep(5)
    # print driver.page_source
    driver.find_element_by_id("TPL_username_1").clear()
    time.sleep(1)
    driver.find_element_by_id("TPL_password_1").clear()
    time.sleep(1)
    driver.find_element_by_id("TPL_username_1").send_keys('hengwei@starmerx.com')
    time.sleep(1)
    driver.find_element_by_id("TPL_password_1").send_keys('tianhu2016')
    time.sleep(1)
    driver.find_element_by_id("J_SubmitStatic").click()

    # time.sleep(5)  # 等待滑动模块和其他JS文件加载完毕！
    # while True:
    #     try:
    #         # 定位滑块元素
    #         source = driver.find_element_by_xpath("//*[@id='nc_1_n1z']")
    #         # 定义鼠标拖放动作
    #         ActionChains(driver).drag_and_drop_by_offset(source, 400, 0).perform()
    #         # 等待JS认证运行,如果不等待容易报错
    #         time.sleep(2)
    #         # 查看是否认证成功，获取text值
    #         text = driver.find_element_by_xpath("//div[@id='nc_1__scale_text']/span")
    #         # 目前只碰到3种情况：成功（请在在下方输入验证码,请点击图）；无响应（请按住滑块拖动)；失败（哎呀，失败了，请刷新）
    #         if text.text.startswith(u'请在下方'):
    #             print('成功滑动')
    #             break
    #         if text.text.startswith(u'请点击'):
    #             print('成功滑动')
    #             break
    #         if text.text.startswith(u'请按住'):
    #             continue
    #     except Exception as e:
    #         # 这里定位失败后的刷新按钮，重新加载滑块模块
    #         driver.find_element_by_xpath("//div[@id='havana_nco']/div/span/a").click()
    #         print(e)
    # driver.find_element_by_id("J_SubmitStatic").click()
    # print driver.current_url
    # print driver.page_source

    # driver.find_element_by_css_selector("a.forget-pwd J_Quick2Static").click()
    # driver.get_screenshot_as_file('./ffff')

    # driver.get_cookies()  # 取得cookie
    # cookie = "; ".join([item["name"] + "=" + item["value"] + "\n" for item in driver.get_cookies()])
    # print cookie
    # headers = {'cookie': cookie}

    # driver.quit()

if __name__ == '__main__':
    signTaoBao()
    url_file = ALL_CONFIG.SUPPLIERURL_FILE
    star(url_file)

