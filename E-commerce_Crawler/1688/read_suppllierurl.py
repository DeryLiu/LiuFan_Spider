from Tools import ALL_CONFIG
from selenium import webdriver
import re
import time
driver = webdriver.PhantomJS(executable_path=ALL_CONFIG.PHANTOMJS_PATH)
driver.get('https://login.taobao.com/member/login.jhtml?style=b2b&css_style=b2b&from=b2b&newMini2=true&full_redirect=true&redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253Dhttp%25253A%25252F%25252Fmember.1688.com%25252Fmember%25252Foperations%25252Fmember_operations_jump_engine.htm%25253Ftracelog%25253Dlogin%252526operSceneId%25253Dafter_pass_from_taobao_new%252526defaultTarget%25253Dhttp%2525253A%2525252F%2525252Fwork.1688.com%2525252F%2525253Ftracelog%2525253Dlogin_target_is_blank_1688&reg=http%3A%2F%2Fmember.1688.com%2Fmember%2Fjoin%2Fenterprise_join.htm%3Flead%3Dhttp%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252Fmember_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253Dafter_pass_from_taobao_new%2526defaultTarget%253Dhttp%25253A%25252F%25252Fwork.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688%26leadUrl%3Dhttp%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252Fmember_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253Dafter_pass_from_taobao_new%2526defaultTarget%253Dhttp%25253A%25252F%25252Fwork.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688%26tracelog%3Dmember_signout_signin_s_reg')

# login TaoBaomn
driver.find_element_by_id("TPL_username_1").clear()
driver.find_element_by_id("TPL_password_1").clear()
driver.find_element_by_id("TPL_username_1").send_keys('hengwei@starmerx.com')
driver.find_element_by_id("TPL_password_1").send_keys('tianhu2016')

driver.find_element_by_id("J_SubmitStatic").click()

driver.get_cookies()
cookie = "; ".join([item["name"] + "=" + item["value"] + "\n" for item in driver.get_cookies()])

lal = []
aaa = open('./need_to_transfer.csv','r')
for a in aaa:
    print (a)
    if '/creditdetail' not in a:
        time.sleep(2.5)
        try:
            text_url = 'http' + a.split('http')[1]
        except:
            pass
        print (text_url)
        # html = get_html.get_html(text_url)
        driver.get(text_url)
        html = driver.page_source
        url_fr = re.findall(r'<li class=" " data-page-name="creditdetail">(.*?)</li>',html,re.S)
        print (url_fr)
        print (a)
        try:
            url = str(url_fr).split('href="http')[1]
            url = url.split('?')[0]
            info = a.split('http')[0] + url
            lal.append(info)
        except:
            print (11)
        time.sleep(5.45)
    else:
        lal.append(a)

print (lal)
driver.quit()
for lalal in lal:
    with open('./5789.txt','aw') as jklj:
        jklj.write(lalal+'\n')