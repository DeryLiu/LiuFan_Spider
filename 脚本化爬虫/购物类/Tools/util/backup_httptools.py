#/use/bin/env python
#-*-coding:utf-8-*-
'''
httptools by al
'''
import urllib2
import os
import random
class httptools:
    def __init__(self,market):
        self.__head={}
        self.__cookie='x-wl-uid=1O+c73xzpqlWx2sDgPx08AgYfGZQekebp5Lf1L3VHFVtKbRino8oS15llxjgqz6HpnNFKtUiq94k=; session-token=U8xc+ipixklSYCehsRfK5WITsswpszDkF7GW1EAX3L+txjHcNsrIpFUoIYK2CNhHfiU3c5Qxz8pWqP16giA2T27hmFOBNAf3HPr0xaHnm4ug/mUOJDRBYpyOvTy+rmrCbndVXGirxFaJiAw7Iu0piJ3VBQO29FOQrG9meTZRcXBVs/H3Rj3ngi4xHnhPhej6TKUkQ57XrEbtP3QDFcEQFhYHTfT70x/8r3YtL3NmLdhqIp79m9B7BXd3sxb9CFYBOm7D9mouYts=; s_cc=true; s_vnum=1858562387501%26vn%3D1; s_ppv=100; s_nr=1426562436088-New; s_dslv=1426562436093; s_sq=acsca-prod%3D%2526pid%253D200285890%2526pidt%253D1%2526oid%253Djavascript%25253Awindow.close%252528%252529%25253B%2526ot%253DA; amznacsleftnav-cf97d5fc-1402-4423-8219-eaa3902f6480=1; session-id-time=2082787201l; session-id=187-6418283-2109867; ubid-acbca=190-7395036-6258911; csm-hit=s-02427XBCVJS730BKGC92|1426580456730'
        self.__head['Accept']='get_price_url/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
#		self.__head['Accept-Charset']=''
#		self.__head['Accept-Encoding']='gzip,deflate,sdch'
        self.__head['Accept-Language']='en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4'
        self.__head['Cache-Control']='max-age=0'
        # self.__head['Referer']='http://www.amazon.com/'
#		self.__head['Authorization']=''
        self.__head['Connection']='keep-alive'
#		self.__head['Content-Length']=''
        # self.__head['Cookie']=self.__cookie
#        self.__head['Host']='www.amazon.com'
        self.__head['Host']='www.amazon.' + market
#		self.__head['Pragma']=''
#		self.__head['Referer']=''
        self.__head['User-Agent']='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        self.__proxylist=None
    def gethtml(self,url,data=None,heads='FHBJ<KGFYOLL'):
#         print url
        if heads=='FHBJ<KGFYOLL':
            heads=self.__head
        if not heads:
            heads={}
        content=''
        count=0
        while True:
            try:
                req=urllib2.Request(url,data,heads)
                content=urllib2.urlopen(req,timeout=10).read()
                return content
            except Exception,e:
                print e
                count+=1
                if "404" in str(e):
                    return '404 error'
#                     return str(e)
                if count==3:
                    return 'time out or other errors'
#                     return str(e)
    def sgethtml(self,url,data=None,heads='FHBJ<KGFYOLL'):
        return self.gethtml(self,url,data=None,heads=None)
    def gethtmlproxy(self,url,data=None,heads='FHBJ<KGFYOLL'):
        if not self.__proxylist:
            if os.path.exists('./myutil/proxylist.txt'):
                f=open('./myutil/proxylist.txt')
            else:
                f=open('proxylist.txt')
            self.__proxylist=f.readlines()
            f.close()
#         proxy_support = urllib2.ProxyHandler({'http':'http://50.2.15.204:8800'})
        if heads=='FHBJ<KGFYOLL':
            heads=self.__head
        if not heads:
            heads={}
        count=0
        while True:
            try: 
                proxy_support = urllib2.ProxyHandler({'http':'http://'+random.choice(self.__proxylist)})
                opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)  
                urllib2.install_opener(opener)             
                req=urllib2.Request(url,data,heads)
                res = urllib2.urlopen(req,timeout=10)
                content = res.read()  
                if -1== content.find('Sorry, we just need to make sure you') or count > 5:
#                 req=urllib2.Request(url,data,heads)
#                 res=urllib2.urlopen(req,timeout=10)
#                 content=res.read()
                    count+=1
                    return content
            except Exception,e:
                print e
                count+=1
                if "404" in str(e):
                    return '404 error'
#                     return str(e)
                if count==6:
                    return 'time out or other errors'
#                     return str(e)
    def sgethtmlproxy(self,url):
        return self.gethtmlproxy(self,url,data=None,heads=None)