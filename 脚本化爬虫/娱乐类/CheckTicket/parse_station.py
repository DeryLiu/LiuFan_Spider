# 我们运行这个脚本，它将以字典的形式返回所有车站和它的大写字母代号, 我们将结果重定向到 stations.py
# python3 parse_station.py > stations.py
import re
import requests
from pprint import pprint

# 从12306源码里找到的js文件，包含所有站点和简写的对应。
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8971'
response = requests.get(url, verify=False)
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
pprint(dict(stations), indent=4)