#!/usr/bin/python
# coding=utf8

import re
import os
import gzip
import sys
import time
import socket
import random
import urllib2
import cookielib
import StringIO
import urlparse
from abc import abstractmethod
from httplib import IncompleteRead, HTTPResponse

import configparser
import gc
import simplejson as json


__author__ = 'Alex Yu'
__version__ = '0.1.0'


def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except IncompleteRead, e:
            return ''.join(e.partial)
    return inner
HTTPResponse.read = patch_http_response_read(HTTPResponse.read)


def get_date():
    return time.strftime("%Y-%m-%d", time.localtime())


def get_now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def log_error(func):
    """
    Decorator to log exceptions
    :param func:
    :return: None if error
    """

    def wrapper(*args, **kwargs):
        result = None
        try:
            # st = time.time()
            result = func(*args, **kwargs)
            # print '%s: %s' % (func.__name__, time.time() - st)
        except Exception as e:
            filename = sys._getframe().f_code.co_filename
            msg = '%s: Exception at file %s function %s.\tMessage: %s\n' % (get_now(), filename, func.__name__, e)
            with open('log_%s.log' % get_date(), 'a') as f:
                f.write(msg)
        return result

    return wrapper


class Spider(object):
    """
    Spider
    """

    def __init__(self, config_file=None):
        """
        Initial params
        :param config_file: Config file path
        """
        self.category_keys = set()      # 已获得分类key值，用来判重
        self.category_urls = set()      # 待抓取分类链接
        self.product_keys = set()       # 已获得产品key值，用来判重
        self.product_urls = set()       # 待抓取产品链接
        self.category_per_page = 200
        self.category_urls_file = None
        self.product_urls_file = None
        self.category_list_url = None
        self.product_list_url = None
        self.product_detail_url = None
        self.update = None
        self.space_reg = re.compile(r'[\t\r\n]*')
        self.comment_reg = re.compile(r'<!--.*?-->')
        self.html_reg = re.compile(r'<[^>]+>')
        self.number_reg = re.compile(r'\d+\.?\d*')
        self.character_entities = {
            '&nbsp;': '',
            '&lt;': '<',
            '&gt;': '>',
            '&amp;': '&',
            '&quot;': '"',
            '&apos;': '`',
            '&cent;': '￠',
            '&pound;': '£',
            '&yen;': '¥',
            '&euro;': '€',
            '&sect;': '§',
            '&copy;': '©',
            '&reg;': '®',
            '&trade;': '™',
            '&times;': '×',
            '&divide;': '÷'
        }
        self.category_top_reg = None
        self.category_reg = None
        self.category_key_value_reg = None
        self.category_leaf_reg = None
        self.category_list_count_reg = None
        self.category_a_tag_reg = None
        self.product_reg = None
        self.product_key_value_reg = None
        self.product_a_tag_reg = None
        self.product_next_page_reg = None

        self.uas = []
        self.proxies = []
        self.proxy_sequence = random.randint(0, 250)
        self.headers = {}
        self.download_file = False
        self.result_path = None
        self.load_configs(config_file)

    def init_result_path(self, name='spider'):
        if self.result_path is None:
            self.result_path = 'results/' + name + time.strftime('/%Y/%m%d/', time.localtime(time.time()))
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)

    # @log_error
    def load_configs(self, path):
        """
        从文件中加载配置
        :param path: 配置文件
        :return:
        """
        conf = configparser.ConfigParser()
        conf.read(path)

        # Try to parse urls
        self.category_per_page = conf.getint('urls', 'category_per_page')
        if self.category_per_page is None:
            self.category_per_page = 50
        self.category_list_url = conf.get('urls', 'category_list_url')
        self.product_list_url = conf.get('urls', 'product_list_url')
        self.product_detail_url = conf.get('urls', 'product_detail_url')

        # Set fetch mode: '1' to fetch all stuffs and others to fetch new stuffs
        # self.update = conf.getint('modes', 'update')

        # Load files
        self.load_category_keys(conf.get('files', 'category_keys'))
        self.category_urls_file = conf.get('files', 'category_urls')
        self.product_urls_file = conf.get('files', 'product_urls')
        self.load_product_keys(conf.get('files', 'product_keys'))
        self.load_uas(conf.get('files', 'ua_file'))
        self.load_proxies(conf.get('files', 'proxy_file'))
        self.load_headers(conf.get('files', 'header_file'))
        self.update = len(self.product_keys) == 0

        # Try to parse regulars
        self.category_top_reg = re.compile(conf.get('regulars', 'category_top_reg'), re.I)
        self.category_reg = re.compile(conf.get('regulars', 'category_reg'), re.I)
        self.category_key_value_reg = re.compile(conf.get('regulars', 'category_key_value_reg'), re.I)
        self.category_leaf_reg = re.compile(conf.get('regulars', 'category_leaf_reg'), re.I)
        self.category_list_count_reg = re.compile(conf.get('regulars', 'category_list_count_reg'), re.I)
        self.category_a_tag_reg = re.compile(conf.get('regulars', 'category_a_tag_reg'), re.I)
        self.product_reg = re.compile(conf.get('regulars', 'product_reg'), re.I)
        self.product_key_value_reg = re.compile(conf.get('regulars', 'product_key_value_reg'), re.I)
        self.product_a_tag_reg = re.compile(conf.get('regulars', 'product_a_tag_reg'), re.I)
        self.product_next_page_reg = re.compile(conf.get('regulars', 'product_next_page_reg'), re.I)

    # @log_error
    def load_category_keys(self, path):
        with open(path, 'r') as f:
            self.category_keys = set(item.replace('\n', '').replace('\r', '') for item in f if item.replace('\n', '').replace('\r', ''))

    # @log_error
    def load_product_keys(self, path):
        with open(path, 'r') as f:
            self.product_keys = set(item.replace('\n', '').replace('\r', '') for item in f if item.replace('\n', '').replace('\r', ''))

    # @log_error
    def load_uas(self, path):
        with open(path, 'r') as f:
            self.uas = [line.replace('\r', '').replace('\n', '').strip() for line in f]

    # @log_error
    def load_proxies(self, path):
        with open(path, 'r') as f:
            self.proxies = [line.replace('\r', '').replace('\n', '').strip() for line in f]

    # @log_error
    def load_headers(self, path):
        with open(path, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                key, value = line.split('\t')
                self.headers[key.strip()] = value.strip()

    # @log_error
    def get_random_ua(self):
        return self.uas and random.choice(self.uas) or ''

    # @log_error
    def get_random_proxy(self):
        proxy = self.proxies and {'http': 'http://%s' % random.choice(self.proxies)} or None
        return proxy

    def get_proxy(self):
        if self.proxies:
            seq = self.proxy_sequence
            self.proxy_sequence += 1
            return {'http': 'http://%s' % self.proxies[seq % len(self.proxies)]}
        return None

    # @log_error
    def get_headers(self):
        headers = self.headers
        headers['User-Agent'] = self.get_random_ua()
        return headers

    # @log_error
    def get_handlers(self):
        # proxy_support = urllib2.ProxyHandler(self.get_random_proxy())
        proxy_support = urllib2.ProxyHandler(self.get_proxy())
        cj = cookielib.CookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        return proxy_support, cookie_support, urllib2.HTTPHandler, urllib2.HTTPSHandler

    # @log_error
    def get_url_html(self, url, retry=3, retry_sleep_time=3, retry_word=None, timeout=30, referer=None, store_page=False, store_folder=None):
        html, msg = None, None
        while retry > 0:
            time.sleep(random.randint(1, retry_sleep_time))
            print 'Get url: %s (%s retry left)' % (url, retry)
            try:
                opener = urllib2.build_opener(*self.get_handlers())
                headers = self.get_headers()
                if referer is not None:
                    headers['Referer'] = referer
                req = urllib2.Request(url, headers=headers)
                response = opener.open(req, timeout=timeout)
                html = response.read()
                if headers['Accept-Encoding'] and 'gzip' in headers['Accept-Encoding']:
                    data = StringIO.StringIO(html)
                    try:
                        with gzip.GzipFile(fileobj=data) as gz:
                            html = gz.read()
                    except Exception as e:
                        pass
                html = self.space_reg.sub(r'', html)            # remove '\t's and '\n's
                html = self.comment_reg.sub(r'', html)          # remove comments
                if retry_word is not None and retry_word in html:
                    # retry -= 1
                    html, msg = None, '%s\t%s\t%s' % (get_now(), url, '出现“重试”字符串: %s' % retry_word)
                    print msg
                else:
                    if store_page:
                        if store_folder is None:
                            store_folder = './htmls/'
                        if not os.path.exists(store_folder):
                            os.mkdir(store_folder)
                        with open(store_folder + url.replace('/', '_') + '.html', 'wt') as f:
                            f.write(html)
                    break
            except (urllib2.URLError, socket.timeout, socket.error) as e:
                retry -= 1
                html, msg = None, '%s\t%s\t%s' % (get_now(), url, e.message)
            except Exception as e:
                retry -= 1
                html, msg = None, '%s\t%s\t%s' % (get_now(), url, e.message)
        if html is None:
            print msg
            with open('fail_urls.txt', 'a') as f:
                f.write('%s\n' % url)
        return html

    # @log_error
    def clean_html_tag(self, html):
        """
        去除网页中的html标签
        :param html: 原始的网页
        :return: 去除了html标签的网页
        """
        html = self.html_reg.sub('', html)
        for k, v in self.character_entities.items():
            html = html.replace(k, v)
        return html

    # @log_error
    def make_page_url(self, key, value):
        """
        根据key,value构造产品列表链接
        :param value:
        :param key:
        :return:
        """
        return self.product_list_url.replace('[key]', key).replace('[value]', value)

    # @log_error
    def make_product_url(self, key, value):
        """
        生成产品链接地址
        :param key:
        :param value:
        :return:
        """
        return self.product_detail_url.replace('[key]', key).replace('[value]', value)

    # @log_error
    def get_category_key_value(self, url):
        m = self.category_key_value_reg.search(url)
        if m:
            kv_dict = m.groupdict()
            return kv_dict['key'], kv_dict['value']
        return None, None

    def get_product_key_value(self, url):
        m = self.product_key_value_reg.search(url)
        return m and (m.groupdict()['key'], m.groupdict()['value']) or (None, None)

    # @log_error
    def retrieve_product_info(self, html):
        """
        从html中提取需要产品数据
        :param html:
        :return:
        """
        return {}

if __name__ == '__main__':
    spider = Spider('spider.conf')
    u = 'https://www.amazon.com/Best-Sellers-Collectible-Coins-Individual/zgbs/coins/9003133011/ref=zg_bs_nav_coins_col_1_coins_col'
    print spider.get_category_key_value(u)
