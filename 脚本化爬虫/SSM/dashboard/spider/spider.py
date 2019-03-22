#!/usr/bin/python
# coding=utf8

import re
import os
import sys
import time
import socket
import random
import urllib2
import cookielib
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
        except IncompleteRead as e:
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
        self.category_reg = None
        self.category_top_reg = None
        self.category_key_value_page_reg = None
        self.category_children_reg = None
        self.category_list_count_reg = None
        self.category_a_tag_reg = None
        self.product_reg = None
        self.product_a_tag_reg = None
        self.product_next_page_reg = None

        self.uas = []
        self.proxies = []
        self.headers = {}
        self.download_file = False
        self.load_configs(config_file)

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
        self.product_urls_file = conf.get('files', 'product_urls')
        self.load_uas(conf.get('files', 'ua_file'))
        self.load_proxies(conf.get('files', 'proxy_file'))
        self.load_headers(conf.get('files', 'header_file'))
        self.update = len(self.product_keys) == 0

        # Try to parse regulars
        self.category_reg = re.compile(conf.get('regulars', 'category_reg'))
        self.category_top_reg = re.compile(conf.get('regulars', 'category_top_reg'))
        self.category_key_value_page_reg = re.compile(conf.get('regulars', 'category_key_value_page_reg'))
        self.category_children_reg = re.compile(conf.get('regulars', 'category_children_reg'))
        self.category_list_count_reg = re.compile(conf.get('regulars', 'category_list_count_reg'))
        self.category_a_tag_reg = re.compile(conf.get('regulars', 'category_a_tag_reg'))
        self.product_reg = re.compile(conf.get('regulars', 'product_reg'))
        self.product_a_tag_reg = re.compile(conf.get('regulars', 'product_a_tag_reg'))
        self.product_next_page_reg = re.compile(conf.get('regulars', 'product_next_page_reg'))

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
                key, value = line.split(',')
                self.headers[key.strip()] = value.strip()

    # @log_error
    def get_random_ua(self):
        return self.uas and random.choice(self.uas) or ''

    # @log_error
    def get_random_proxy(self):
        return self.proxies and {'http': 'http://%s' % random.choice(self.proxies)} or None

    # @log_error
    def get_headers(self):
        headers = self.headers
        headers['User-Agent'] = self.get_random_ua()
        return headers

    # @log_error
    def get_handlers(self):
        proxy_support = urllib2.ProxyHandler(self.get_random_proxy())
        cj = cookielib.CookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        return proxy_support, cookie_support, urllib2.HTTPHandler, urllib2.HTTPSHandler

    # @log_error
    def get_url_html(self, url, retry=3, retry_sleep_time=3, timeout=30):
        # print 'Get url: %s' % url
        opener = urllib2.build_opener(*self.get_handlers())
        req = urllib2.Request(url, headers=self.get_headers())
        html, msg = None, None
        while retry > 0:
            try:
                response = opener.open(req, timeout=timeout)
                html = response.read()
                html = self.space_reg.sub(r'', html)            # remove '\t's and '\n's
                html = self.comment_reg.sub(r'', html)          # remove comments
            except (urllib2.URLError, socket.timeout, socket.error) as e:
                msg = e.message
                time.sleep(retry_sleep_time)
                retry -= 1
                html = None
                print(e)
            except Exception as e:
                msg = e.message
                time.sleep(retry_sleep_time)
                retry -= 1
                html = None
                print(e)
            else:
                break
        if html is None:
            print('%s\t%s\t%s' % (get_now(), url, msg))
        return html

    # @log_error
    def clean_html_tag(self, html):
        html = self.html_reg.sub('', html)
        for k, v in self.character_entities.items():
            html = html.replace(k, v)
        return html

    # @log_error
    def make_page_url(self, key, value):
        """
        从html中提取下一页的链接地址
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
    def get_leaf_category_urls(self, url):
        leaf_urls = set()
        urls = set()
        urls.add(url)
        urls_old = set()
        not_leaf_urls = set()
        while urls:
            u = urls.pop()
            urls_old.add(u)
            html = self.get_url_html(u)
            lus = self.category_children_reg.findall(html)
            lus = [l for l in lus if l not in (urls_old | leaf_urls)]
            if lus:
                not_leaf_urls.add(u)
                urls.update(lus)
                leaf_urls.update(lus)
            # else:
            #     leaf_urls.add(u)
        return leaf_urls - not_leaf_urls

    # @log_error
    def get_category_key_value(self, url):
        m = self.category_key_value_page_reg.search(url)
        if m:
            kv_dict = m.groupdict()
            return kv_dict['key'], kv_dict['value']
        return None, None

    # @log_error
    def get_product_urls(self, html):
        """
        从html中提取需要的信息，写入self.product_keys
        只记录key
        :param html:
        :return:
        """
        html = html[:html.find('class="lvresult clearfix li"')]
        product_a_tags = self.product_a_tag_reg.findall(html)
        print('find %s products' % len(product_a_tags))
        urls = set()
        for a_tag in product_a_tags:
            product_dict = self.product_reg.search(a_tag).groupdict()
            urls.add(self.make_product_url(product_dict['key'], product_dict['value']))
        return urls

    # @log_error
    def get_category_product_total(self, html):
        match = self.category_list_count_reg.search(html)
        return match and int(match.group(1)) or 0

    # @log_error
    def get_list_page_next_url(self, html, **kwargs):
        """
        提取页面下的下一页分页地址
        :param kwargs:
        :param html:
        :return:
        """
        curl_url = kwargs.get('cur_url')
        total = self.get_category_product_total(html)
        if total > 0 and curl_url is not None:
            last_page = (total / self.category_per_page) + 1
            _, _, cur_page = self.get_category_key_value(curl_url)
            if cur_page is not None and cur_page < last_page:
                next_page = cur_page + 1
                clean_url = curl_url.split('?')[0]
                # http://www.ebay.com/sch/Far-Eastern/162916/i.html?_mPrRngCbx=1&_udlo=0&_udhi=300&_pgn=2&_skc=100&rt=nc
                return clean_url + '?_pgn=%s&_skc=%s&rt=nc' % (next_page, (next_page - 1) * self.category_per_page)

    # @log_error
    @abstractmethod
    def retrieve_product_info(self, html):
        """
        从html中提取需要产品数据
        :param html:
        :return:
        """
        return {}

    @log_error
    def crawl_products(self):
        """
        抓取产品，保存数据到文件中
        :return:
        """
        while self.product_urls:
            values = {}
            url = self.product_urls.pop()
            match = self.product_reg.search(url)
            if match:
                key = match.groupdict().get('key')
                values.update({
                    'product_id': key,
                    'url': url
                })
                html = self.get_url_html(url)
                if html is not None:
                    info = self.retrieve_product_info(html)
                    if info is not None:
                        values.update(info)
                        # TODO: 处理获得的产品信息


if __name__ == '__main__':
    spider = Spider('spider.conf')
