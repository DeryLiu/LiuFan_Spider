# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
from url_proxy import get_url,get_proxy,put_db
import time
import random
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
urls = get_url()
#proxys = get_proxy()



def get_data_main():
	
	def get_json(content):
		print(u'开始获取soup')
		soup = BeautifulSoup(content,'html.parser')
		jbxx = {}
		#表格中基本信息(4)：
		a = soup.find('div', class_="baseInfo_model2017").find('tbody').find_all('td')
		#法人代表
		frdb = a[0].find('a').text
		jbxx[u'法人代表'] = frdb
		#注册资本
		zczb = a[1].text
		jbxx[u'注册资本'] = zczb
		#注册时间
		zcsj = a[2].text
		jbxx[u'注册时间'] = zcsj
		#经营状态
		jyzt = a[3].text
		jbxx[u'经营状态'] = jyzt
		
		print(u'获取余下json信息')
		#余下信息(10)：
		b = soup.find('div', class_="row b-c-white company-content base2017").find('tbody').find_all('div',class_='c8')
		for i in b:
			#print i.text
			c = i.text.split(u'：')
			#print len(c)
			jbxx[c[0]]=c[1]
		jbxx_js = json.dumps(jbxx,ensure_ascii=False)	
		return jbxx_js
	
		
	
	def get_data(driver):
		while not len(urls) == 0:
			try:
				com = urls[0]
				company = com[0]
				url = com[1]
				print(u'开始请求链接%s'%url)
				try:
					driver.get(url)
				except:
					print(u'加载时间太长了，可能会有问题')
					driver.execute_script("window.stop()")
				driver.save_screenshot(r'%s.png'%company)
				time.sleep(5)
				driver.save_screenshot(r'%s5.png'%company)
				content = driver.page_source.encode('utf-8')		
				jbxxjs = get_json(content)
			except:
				print(u'在%s请求页面异常，换个代理'%company)
				get_data_main()
				driver.close()
			else:
				print(u'信息已经获取，准备入库')
				put_db(company,jbxxjs)
				urls.pop(0)
				print(u'%s入库成功'%company)
				
	#proxies = str(proxys[0].strip())
	#proxys.pop(0)
	proxies = '94.177.240.167:1189'
	print(u'当前代理为%s'%proxies)
	try:
		dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)
		dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0")
		#dcap["phantomjs.page.settings.resourceTimeout"] = ("10")
		dcap["phantomjs.page.settings.loadImages"] = False 
		service_args = [
			'--proxy='+proxies
			] #默认为http代理，可以指定proxy type
		print service_args[0]
		driver = webdriver.PhantomJS(service_args=service_args, desired_capabilities=dcap)
		#设置延时10秒
		driver.set_page_load_timeout(60)
		driver.set_script_timeout(60)
		'''
		login_url = 'http://www.tianyancha.com/login'
		print(u'开始登陆')
		try:
			driver.get(login_url)
		except:
			print(u'加载时间太长了，可能会有问题')
			driver.execute_script("window.stop()")
		#driver.save_screenshot(r'%s.png'%(proxies[0:2]))
		time.sleep(3)
		print(u'输入用户名')
		driver.find_element_by_css_selector('div.pb30.position-rel > input').clear()
		driver.find_element_by_css_selector('div.pb30.position-rel > input').send_keys('13761631397')
		print(u'输入密码')
		driver.find_element_by_css_selector('div.pb40.position-rel > input').clear()
		driver.find_element_by_css_selector('div.pb40.position-rel > input').send_keys('asdfg12345')
		driver.find_element_by_class_name('login_btn').click()
		print('login')
		'''
	except Exception as e:
		print(u'登陆异常%s'%e)
		get_data_main()
	else:
		get_data(driver)
	finally:
		driver.close()	
	
if __name__=='__main__':
	get_data_main()