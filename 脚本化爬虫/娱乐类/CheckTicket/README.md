###代码结构：
- tickets.py 主文件
- parse_station.py  以字典的形式返回所有车站和它的大写字母代号
     
####使用方法：
- 用户只要输入出发站，到达站以及日期就让就能获得想要的信息，比如要查看10月30号上海-北京的火车余票， 我们只需输入：
```python tickets.py 上海 北京 2016-10-30```
    即：```python tickets from to date```
- 火车有各种类型，高铁、动车、特快、快速和直达，我们希望可以提供选项只查询特定的一种或几种的火车，所以，我们应该有下面这些选项：
    -g 高铁
    -d 动车
    -t 特快
    -k 快速
    -z 直达
    这几个选项应该能被组合使用，所以，最终我们的接口应该是这个样子的：
```python tickets.py [-gdtkz] from to date```


####需要的库：
- requests，使用 Python 访问 HTTP 资源的必备库。
- docopt，Python3 命令行参数解析工具。
- prettytable， 格式化信息打印工具，能让你像 MySQL 那样打印数据。
- colorama，命令行着色工具

####解析url
- url地址：https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate=2017-02-23&from_station=SHH&to_station=BJP
    基地址：https://kyfw.12306.cn/otn/lcxxcx/query?
    后缀四个参数：
        - purpose_codes（票种）
        - queryDate （查询日期）
        - from_station （出发地）
        - to_station （目的地）
- 目的地数据的js：https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8997
