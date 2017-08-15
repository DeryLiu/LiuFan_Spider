import logging
import random
import threading
import requests
import ujson
import pymysql

# from modules.Proxy import Proxy

logger = logging.getLogger()

class ProxyProvider:
    def __init__(self, min_proxies=200):
        self._bad_proxies = {}
        self._minProxies = min_proxies
        self.lock = threading.RLock()
        self.db = pymysql.connect("localhost","root","123456","Spider_Data",charset='utf8')
        self.cursor = self.db.cursor()

        self.get_list()

    def get_list(self):
        logger.debug("Getting proxy list")
        sql = "SELECT * FROM proxies_info;"
        proxies_list = []
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            for row in results:
                proxy_ip = row[1]
                proxy_port = str(row[2])
                proxies_list.append(proxy_ip + ':' + proxy_port)
        except:
            self.db.rollback()
            print('db error')

        # r = requests.get("https://jsonblob.com/api/jsonBlob/31bf2dc8-00e6-11e7-a0ba-e39b7fdbe78b", timeout=10)
        # proxies = ujson.decode(r.text)
        logger.debug("Got %s proxies", len(proxies_list))
        self._proxies = list(map(lambda p: Proxy_Socre(p), proxies_list))

    def pick(self):
        with self.lock:
            self._proxies.sort(key = lambda p: p.score, reverse=True)
            proxy_len = len(self._proxies)
            max_range = 50 if proxy_len > 50 else proxy_len
            proxy = self._proxies[random.randrange(1, max_range)]
            proxy.used()
            return proxy

    def count(self):
        with self.lock:
            return len(self._proxies)

class Proxy_Socre:
    def __init__(self, url):
        self._url = url
        self._score = 0
        pass

    @property
    def url(self):
        return self._url

    def used(self):
        self._score += 1

    def fatal_error(self):
        self._score -= 10

    def connection_error(self):
        self._score -= 2

    def parse_error(self):
        self._score -= 2

    @property
    def score(self):
        return self._score


if __name__ == "__main__":
    provider = ProxyProvider()
    print(provider.pick().url)
    # provider.get_list()
