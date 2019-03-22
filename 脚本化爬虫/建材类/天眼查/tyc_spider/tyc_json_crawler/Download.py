# -*- coding:utf-8 -*-
import requests
import pymysql
import random

class download():

	def __init__(self,a):
		conn = pymysql.connect(host='127.0.0.1', user='root', password='123', db='db', port=3306, charset='utf8')
		cur = conn.cursor()
		self.a=a
		m = str(self.a)
		sql = 'SELECT ip,port FROM proxy_db LIMIT %s,30'%m
		cur.execute(sql)
		proxys = cur.fetchall()
		cur.close()
		conn.close()
		proxies = []
		for p in proxys:
			self.ip = p[0]
			self.port = p[1]
			self.proxy = 'http://'+self.ip+':'+self.port
			proxies.append(self.proxy)
			self.proxies = proxies

		self.user_agent_list = [
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
			"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
			"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
			"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
			"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
		]



	def get(self,url):

		agent = random.choice(self.user_agent_list)
		#headers = {'content-type': 'application/json','User-Agent': agent}
		#headers = {"token":"token=e50970f36b5d4be988eae8b2f10d"}
		# 加一个控制，队列无数据或小于多少时，init一下，重新从数据库获取最新代理ip
		if len(self.proxies) == 10:
			self.a+=20
			a=self.a
			self.__init__(a)

		IP = self.proxies[0]
		proxy = {'http':IP}
		print(u'当前代理为%s' %IP)
		try:
			response = requests.get(url,proxies=proxy)
			if response.status_code == 200:
				return response
			else:
				print (u'网页请求错误%s'%response.status_code)
				#with open('proxy_err.txt', 'a') as pe:
				#	pe.write(response.status_code+url+'\n')
				print(u'换个代理加载%s' % url)
				self.proxies.pop(0)
				return self.get(url)
		except Exception as e:
			print(u'换个代理加载%s'%url)
			self.proxies.pop(0)
			return self.get(url)


request = download(3400)

