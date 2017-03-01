# coding=utf-8
from spider import Spider
import re
import urlparse
import simplejson as json
import configparser
from multiprocessing.dummy import Pool


class AmazonSpider(Spider):

    def __init__(self, config_file=None):
        # product_url information regulars
        self.product_name_reg = None
        self.product_rank_reg = None
        self.product_other_ranks_reg = None
        self.product_star_reg = None
        self.product_seller_list_reg = None
        self.product_seller_url_reg = None
        self.product_seller_next_reg = None
        self.product_brand_reg = None
        self.product_image_reg = None
        self.category_child_block_reg = None
        super(AmazonSpider, self).__init__(config_file)

    def load_configs(self, path):
        super(AmazonSpider, self).load_configs(path=path)
        conf = configparser.ConfigParser()
        conf.read(path)
        # Parse product_url info regulars
        self.product_name_reg = re.compile(conf.get('product_info_regulars', 'product_name_reg'))
        self.product_rank_reg = re.compile(conf.get('product_info_regulars', 'product_rank_reg'), re.I)
        self.product_other_ranks_reg = re.compile(conf.get('product_info_regulars', 'product_other_ranks_reg'), re.I)
        self.product_star_reg = re.compile(conf.get('product_info_regulars', 'product_star_reg'), re.I)
        self.product_seller_list_reg = re.compile(conf.get('product_info_regulars', 'product_seller_list_reg'), re.I)
        self.product_seller_url_reg = re.compile(conf.get('product_info_regulars', 'product_seller_url_reg'))
        self.product_seller_next_reg = re.compile(conf.get('product_info_regulars', 'product_seller_next_reg'))
        self.product_brand_reg = re.compile(conf.get('product_info_regulars', 'product_brand_reg'), re.I)
        self.product_image_reg = re.compile(conf.get('product_info_regulars', 'product_image_reg'), re.I)
        self.category_child_block_reg = re.compile(conf.get('regulars', 'category_child_block_reg'), re.I)

    def get_child_categories(self, url):
        html = self.get_url_html(url)
        if html is None:
            return []
        return self.category_a_tag_reg.findall(html)

    def get_leaf_categories(self, url):
        html = self.get_url_html(url)
        if html is None:
            return None
        m = self.category_child_block_reg.search(html)
        html = m and m.group() or None
        if html is None:
            print(u'找到叶子分类: %s' % url)
            return {url}
        urls = self.category_a_tag_reg.findall(html)
        leaf_urls = set()
        for u in urls:
            r = self.get_leaf_categories(u)
            if r is not None:
                leaf_urls.update(r)
            # TODO: remove break
            break
        return list(leaf_urls)

    def get_top_categories(self):
        html = self.get_url_html(self.category_list_url)
        return html and self.category_top_reg.findall(html) or []

    @staticmethod
    def make_top_page_urls(url):
        urls = list()
        page_template = '{url}?pg={page}&ajax=1'
        for i in range(1, 6):
            urls.append(page_template.format(url=url, page=i))
        return urls

    def get_top_100(self, url):
        urls = self.make_top_page_urls(url)
        top_100_urls = list()
        for url in urls:
            html = self.get_url_html(url)
            if html is None:
                return []
            top_100_urls.extend(self.get_page_products(html))
            # TODO: remove break
            break
        return list(set(top_100_urls))

    def get_page_products(self, html):
        products = []
        for product_url in self.product_a_tag_reg.findall(html):
            if not product_url.startswith('http'):
                product_dict = self.product_reg.search(product_url).groupdict()
                key, value = product_dict['key'], product_dict['value']
                product_url = self.make_product_url(key, value)
            if product_url is not None:
                products.append(product_url)
        return products

    def retrieve_product_name(self, html):
        if self.product_name_reg.pattern != '':
            m = self.product_name_reg.search(html)
            return m and m.group(1) or ''
        return ''

    def retrieve_product_rank(self, html, identify_word=None):
        rank = 0
        if identify_word is not None and identify_word in html and self.product_rank_reg.pattern != '':
            m = self.product_rank_reg.search(html)
            try:
                rank = m and int(m.group(1).replace(',', '')) or 0
            except ValueError as e:
                print(u'retrieve_product_rank rank is %s.' % m.group(1))
        return rank

    def retrieve_product_other_ranks(self, html):
        other_ranks = []
        if self.product_other_ranks_reg.pattern != '':
            ranks = self.product_other_ranks_reg.findall(html)
            other_ranks = [{'rank': int(r.replace(',', '')), 'path': self.clean_html_tag(s)} for r, s in ranks]
        return other_ranks

    def retrieve_product_star(self, html):
        if self.product_star_reg.pattern != '':
            m = self.product_star_reg.search(html)
            return m and m.group(1) or ''
        return ''

    def retrieve_product_sellers(self, html, max_rank=None):
        sellers = []
        t = 'https://www.amazon.com/gp/offer-listing/%s/ref=olp_page_1?ie=UTF8&f_new=true&overridePriceSuppression=1&startIndex=%s'
        if max_rank is not None and self.product_seller_list_reg.pattern != '':
            m = self.product_seller_list_reg.search(html)
            asin = m and m.group(1) or None
            if asin is not None:
                url = t % (asin, 0)
                referer = 'https://www.amazon.com/{asin}/dp/{asin}/'.format(asin=asin)
                while True:
                    h = self.get_url_html(url, retry_word='Enter the characters you see below', referer=referer)
                    seller_urls = self.product_seller_url_reg.findall(h)
                    for s, n in seller_urls:
                        sellers.append({'name': n, 'url': 'www.amazon.com/shops/%s' % s})
                    m = self.product_seller_next_reg.search(h)
                    next_index = m and m.group(1) or None
                    if next_index is not None:
                        url = t % (asin, next_index)
                    else:
                        break
        return sellers

    def retrieve_product_brand(self, html):
        if self.product_brand_reg.pattern != '':
            m = self.product_brand_reg.search(html)
            return m and m.group(1) or ''
        return ''

    def retrieve_product_images(self, html):
        if self.product_image_reg.pattern != '':
            return self.product_image_reg.findall(html)
        return []

    def retrieve_product_info(self, html, max_rank=None, identify_word=None):
        if max_rank is None:
            max_rank = 1000
        rank = self.retrieve_product_rank(html, identify_word=identify_word)
        if 0 < rank < max_rank:
            data = dict()
            data['name'] = self.retrieve_product_name(html)
            data['rank'] = rank
            data['other_ranks'] = self.retrieve_product_other_ranks(html)
            data['star'] = self.retrieve_product_star(html)
            data['sellers'] = self.retrieve_product_sellers(html, max_rank=max_rank)
            data['brand'] = self.retrieve_product_brand(html)
            data['images'] = self.retrieve_product_images(html)
            return data
        else:
            return None


if __name__ == '__main__':
    spider = AmazonSpider('amazon.conf')
    url = 'https://www.amazon.com/Anself-Printed-Cartoon-Christmas-Bedding/dp/B01KZK43PW/'
    spider.get_url_html(url, retry=10, retry_sleep_time=3, retry_word='Enter the characters you see below', store_page=True)
