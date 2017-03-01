from multiprocessing import Lock, Pool
from selenium import webdriver
import re
import datetime
from Tools import ALL_CONFIG,get_html

def create_titles(filename, titles):
    f = open(filename, "w")
    f.write("\t".join(titles) + "\n")
    #清除内部缓冲区
    f.flush()
    #关闭文件
    f.close()

def get_json(info):
    driver.implicitly_wait(8)
    try:
        info_url = 'http' + info.split('http')[1]
        basic_info = info.split('http')[0]
        driver.get(info_url)
        html = driver.page_source
        # html = get_html.get_html(url)
        formor_url_list = re.findall(r'<div id="mod-detail-dealrecord"(.*?)"isTgcSKUOffer"',html,re.S)
        formor = str(formor_url_list).split('"remarkListUrl":"')[1]
        formor_url = formor.split('","')[0]
        print (formor_url)
        memberId_list = re.findall(r'<input type="hidden" id="feedbackUid"(.*?)/>',html,re.S)
        memberId = str(memberId_list).split('value="')[1]
        memberId = memberId.split('"')[0]

        memberId_list_1 = re.findall(r'var WolfSmoke={(.*?)}',html,re.S)
        memberId_1 = str(memberId_list_1).split('member_id:"')[1]
        memberId_1 = memberId_1.split('"')[0]
        print (memberId_1)

        json_url = formor_url+'&currentPage=1&memberId='+memberId
        print (json_url)
        data_prime = get_html.get_html(json_url)
        # req = urllib2.Request(json_url)
        # page = urllib2.urlopen(req, timeout=10)
        # data_prime = page.read()
        print (data_prime)
        finally_file = []
        offerSaleRecordStat = data_prime.split('offerSaleRecordStat":')[1]
        offerSaleRecordStat = offerSaleRecordStat.split(',"currentPage"')[0]
        #{"repeatBuyCount":6.5,"buyerTotal":123,"saleRecordTotal":594,"oneRecordRateCountHidden":40,"avgBuyCount":4,"oneRecordRate":6.73},"currentPage":1,"totalPage":29,"defaultShowWithContent":false}
        numlist = re.findall(r'":(.*?),"',str(offerSaleRecordStat),re.S)
        print (numlist)
        finally_file.append(basic_info)
        finally_file.append(numlist)
        lock.acquire()
        result_file.write("\t".join(finally_file) + "\n")
        result_file.flush()
        lock.release()
        driver.implicitly_wait(5)

        driver.close()
    except:
        pass

def star(url_list):
    global result_file,lock,pool
    url_file = open(url_list,'r')
    url_items = url_file.readlines()
    result_file = open(ALL_CONFIG.BUSSINESS_INFO_RESULT_FILE,'aw')
    title = ['repeatBuyCount','buyerTotal','saleRecordTotal','oneRecordRateCountHidden','avgBuyCount','oneRecordRate']
    create_titles('',title)
    print (url_items)
    # for info in url_items:
    #     get_json(info)
    lock = Lock()
    pool = Pool(10)
    # 调用函数把items_list的内容依次传入handle函数中
    pool.map(get_json, url_items)
    pool.close()
    pool.join()

    url_file.close()
    result_file.close()

def signTaoBao():
    # 匿名爬虫
    # 假定9999端口开启tor服务
    global driver
    service_args = ['--proxy=localhost:9999', '--proxy-type=socks5', ]

    driver = webdriver.PhantomJS(executable_path=ALL_CONFIG.PHANTOMJS_PATH)
    driver.get('https://login.taobao.com/member/login.jhtml?style=b2b&css_style=b2b&from=b2b&newMini2=true&full_redirect=true&redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253Dhttp%25253A%25252F%25252Fmember.1688.com%25252Fmember%25252Foperations%25252Fmember_operations_jump_engine.htm%25253Ftracelog%25253Dlogin%252526operSceneId%25253Dafter_pass_from_taobao_new%252526defaultTarget%25253Dhttp%2525253A%2525252F%2525252Fwork.1688.com%2525252F%2525253Ftracelog%2525253Dlogin_target_is_blank_1688&reg=http%3A%2F%2Fmember.1688.com%2Fmember%2Fjoin%2Fenterprise_join.htm%3Flead%3Dhttp%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252Fmember_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253Dafter_pass_from_taobao_new%2526defaultTarget%253Dhttp%25253A%25252F%25252Fwork.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688%26leadUrl%3Dhttp%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252Fmember_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253Dafter_pass_from_taobao_new%2526defaultTarget%253Dhttp%25253A%25252F%25252Fwork.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688%26tracelog%3Dmember_signout_signin_s_reg')

    # login TaoBaomn
    driver.find_element_by_id("TPL_username_1").clear()
    driver.find_element_by_id("TPL_password_1").clear()
    driver.find_element_by_id("TPL_username_1").send_keys('user@starmerx.com')
    driver.find_element_by_id("TPL_password_1").send_keys('key')

    driver.find_element_by_id("J_SubmitStatic").click()

if __name__ == '__main__':
    # url = 'https://detail.1688.com/offer/536552645765.html'
    # # get_PhantomJS_html(url)
    # get_json(url)
    signTaoBao()

    info_list = './bussness_detail.txt'
    star(info_list)