'''
Created on 2012-8-14
@content:amazon api config
@author: zxb
'''

import os
curpath = os.path.join(os.getcwd(), os.path.dirname(__file__)).replace('\\', '/')
root_path = os.path.join(curpath, "../")

proxy_file_name = root_path + 'api_proxylist.txt'

DEFAULT_MAX_TRY = 20

HEADER_LIST = [
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 1.0.3705)',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9) Gecko/2008052906 Firefox/3.0',
                ]

