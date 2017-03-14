import random
import config
import json
import requests


class Html_Downloader(object):
    @staticmethod
    def download(url):
        try:
            r = requests.get(url=url, headers=config.get_header(), timeout=config.TIMEOUT)
            r.encoding = r.content['encoding']
            if (not r.ok) or len(r.content) < 500:
                raise ConnectionError
            else:
                return r.text

        except Exception:
            count = 0  # 重试次数
            proxylist = sqlhelper.select(10)
            if not proxylist:
                return None

            while count < 3:
                try:
                    proxy = random.choice(proxylist)
                    ip = proxy[0]
                    port = proxy[1]
                    proxies = {"http": "http://%s:%s" % (ip, port), "https": "http://%s:%s" % (ip, port)}

                    r = requests.get(url=url, headers=config.get_header(), timeout=config.TIMEOUT, proxies=proxies)
                    r.encoding = r.content['encoding']
                    if (not r.ok) or len(r.content) < 500:
                        raise ConnectionError
                    else:
                        return r.text
                except Exception:
                    count += 1

        return None
