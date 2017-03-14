import requests
from lxml import etree
from bs4 import BeautifulSoup
import config
import re

class Html_Parser(object):

    def XpathPraser(self, response, parser):
        '''
        针对xpath方式进行解析
        :param response:
        :param parser:
        :return:
        '''
        proxylist = []
        root = etree.HTML(response)
        proxys = root.xpath(parser['pattern'])
        for proxy in proxys:
            try:
                ip = proxy.xpath(parser['position']['ip'])[0].text
                port = proxy.xpath(parser['position']['port'])[0].text
                type = 0
                protocol = 0
                # addr = self.ips.getIpAddr(self.ips.str2ip(ip))
                # country = text_('')
                # area = text_('')
                # if text_('省') in addr or self.AuthCountry(addr):
                #     country = text_('国内')
                #     area = addr
                # else:
                #     country = text_('国外')
                #     area = addr
            except Exception as e:
                continue
            # updatetime = datetime.datetime.now()
            # ip，端口，类型(0高匿名，1透明)，protocol(0 http,1 https http),country(国家),area(省市),updatetime(更新时间)

            # proxy ={'ip':ip,'port':int(port),'type':int(type),'protocol':int(protocol),'country':country,'area':area,'updatetime':updatetime,'speed':100}
            proxy = {'ip': ip, 'port': int(port), 'types': int(type), 'protocol': int(protocol), 'country': '',
                     'area': '', 'speed': 100}
            proxylist.append(proxy)
        return proxylist

    def RegularPraser(self, response, parser):
        '''
        针对正则表达式进行解析
        :param response:
        :param parser:
        :return:
        '''
        proxylist = []
        pattern = re.compile(parser['pattern'])
        matchs = pattern.findall(response)
        if matchs != None:
            for match in matchs:
                try:
                    ip = match[parser['position']['ip']]
                    port = match[parser['position']['port']]
                    # 网站的类型一直不靠谱所以还是默认，之后会检测
                    type = 0
                    # if parser['postion']['protocol'] > 0:
                    # protocol = match[parser['postion']['protocol']]
                    # if protocol.lower().find('https')!=-1:
                    #         protocol = 1
                    #     else:
                    #         protocol = 0
                    # else:
                    protocol = 0
                    # addr = self.ips.getIpAddr(self.ips.str2ip(ip))
                    # country = text_('')
                    # area = text_('')
                    # print(ip,port)
                    # if text_('省') in addr or self.AuthCountry(addr):
                    #     country = text_('国内')
                    #     area = addr
                    # else:
                    #     country = text_('国外')
                    #     area = addr
                except Exception as e:
                    continue

                proxy = {'ip': ip, 'port': port, 'types': type, 'protocol': protocol, 'country': '', 'area': '',
                         'speed': 100}

                proxylist.append(proxy)
            return proxylist




