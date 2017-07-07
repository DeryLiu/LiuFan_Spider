# -*- coding:utf-8 -*-
parserList = [
    #66ip
    {
        'urls': ['http://www.66ip.cn/%s.html' % n for n in list(range(1, 11))],
        'type': 'xpath',
        'encode':'gb2312',
        'pattern': "//div[@id='main']/div/div[1]/table/tr[position()>1]",
        'position': {'ip': '/td[1]', 'port': '/td[2]', 'type': '/td[4]', 'protocol': ''}
    },
    #秘密代理
    {
        'urls': ['http://www.mimiip.com/gngao/%s' % n for n in range(1, 10)],
        'type': 'xpath',
        'encode':'utf-8',
        'pattern': "//table[@class='list']/tr",
        'position': {'ip': '/td[1]', 'port': '/td[2]', 'type': '/td[4]', 'protocol': ''}

    },
    #{
    #   'urls': ['http://www.kuaidaili.com/proxylist/%s/' % n for n in range(1, 11)],
    #    'type': 'xpath',
    #    'encode':'utf-8',
    #    'pattern': "//*[@id='index_free_list']/table/tbody/tr[position()>0]",
    #    'position': {'ip': '/td[1]', 'port': '/td[2]', 'type': '/td[3]', 'protocol': '/td[4]'}
    #},
    #ip81
    {
        'urls': ['http://www.ip181.com/daili/%s.html' % n for n in range(1, 11)],
        'type': 'xpath',
        'encode':'gb2312',
        'pattern': "//div[@class='row']/div[3]/table/tbody/tr[position()>1]",
        'position': {'ip': '/td[1]', 'port': '/td[2]', 'type': '/td[3]', 'protocol': '/td[4]'}

    },
    #西刺代理
    {
        'urls': ['http://www.xicidaili.com/wt/%s' %n for n in range(1, 11)],
        'type': 'xpath',
        'encode': 'gb2312',
        'pattern': "//table[@id='ip_list']/tr[position()>1]",
        'position': {'ip': '/td[2]', 'port': '/td[3]', 'type': '/td[5]', 'protocol': '/td[6]'}

    },
    #快代理
    {
        'urls': ['http://www.kuaidaili.com/proxylist/%s/' % n for n in range(1, 11)],
        'type': 'xpath',
        'encode': 'utf-8',
        'pattern': "//tbody/tr",
        'position': {'ip': '/td[1]', 'port': '/td[2]', 'type': '/td[3]', 'protocol': '/td[4]'}

    }
]




