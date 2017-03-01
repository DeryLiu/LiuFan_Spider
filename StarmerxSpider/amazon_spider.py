#!/usr/bin/env python
# coding=utf-8
from spider import Spider
import re
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
        self.product_seller_count_reg = None
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
        self.product_seller_count_reg = re.compile(conf.get('product_info_regulars', 'product_seller_count_reg'))
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
            print('找到叶子分类: %s' % url)
            return {url}
        urls = self.category_a_tag_reg.findall(html)
        leaf_urls = set()
        for u in urls:
            r = self.get_leaf_categories(u)
            if r is not None:
                leaf_urls.update(r)
        return leaf_urls

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
        if identify_word in html and self.product_rank_reg.pattern != '':
            m = self.product_rank_reg.search(html)
            try:
                rank = m and int(m.group(1).replace(',', '')) or 0
            except ValueError as e:
                print('retrieve_product_rank rank is %s.' % m.group(1))
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

    def retrieve_product_seller_count(self, html):
        if self.product_seller_count_reg.pattern != '':
            m = self.product_seller_count_reg.search(html)
            return m and m.group(1) or ''
        return ''

    def retrieve_product_sellers(self, html):
        sellers = []
        t = 'https://www.amazon.com/gp/offer-listing/%s/ref=olp_page_1?ie=UTF8&f_new=true&overridePriceSuppression=1&startIndex=%s'
        if self.product_seller_list_reg.pattern != '':
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
        rank = self.retrieve_product_rank(html, identify_word=identify_word)
        if 0 < rank and (max_rank is None or rank < max_rank):
            data = dict()
            data['name'] = self.retrieve_product_name(html)
            data['rank'] = rank
            data['other_ranks'] = self.retrieve_product_other_ranks(html)
            data['star'] = self.retrieve_product_star(html)
            data['sellers'] = self.retrieve_product_sellers(html)
            # data['sellers'] = self.retrieve_product_seller_count(html)
            data['brand'] = self.retrieve_product_brand(html)
            data['images'] = self.retrieve_product_images(html)
            return data
        else:
            return None


if __name__ == '__main__':
    spider = AmazonSpider('amazon.conf')

    # child_category_urls = spider.get_child_categories('https://www.amazon.com/gp/bestsellers/home-garden')
    #
    # pool = Pool(8)
    # leaf_category_urls = pool.map(spider.get_leaf_categories, child_category_urls)
    # pool.close()
    # pool.join()
    #
    # category_urls = []
    # for urls in leaf_category_urls:
    #     category_urls.extend(urls)
    # with open('category_urls.txt', 'wt') as f:
    #     f.write('\n'.join(category_urls))
    #
    # pool = Pool(8)
    # leaf_category_urls = pool.map(spider.get_top_100, category_urls)
    # pool.close()
    # pool.join()
    #
    # product_urls = []
    # for urls in leaf_category_urls:
    #     product_urls.extend(urls)
    # with open('products.txt', 'wt') as f:
    #     f.write('\n'.join(product_urls))

    product_urls = []
    with open('4.txt') as f:
        for line in f:
            product_urls.append(line.strip())

    def retrieve_products(url):
        html = spider.get_url_html(url, referer=url, retry_word='Enter the characters you see below', store_page=True)
        if html is not None:
            info = spider.retrieve_product_info(html, identify_word='in Home & Kitchen')
            if info is not None:
                info['url'] = url
                with open('amazon_top_products.txt', 'a') as f:
                    f.write('%s\n' % json.dumps(info))
                    f.flush()

    pool = Pool(8)
    try:
        pool.map(retrieve_products, product_urls)
    except TypeError as e:
        print('Error: %s' % e)
    pool.close()
    pool.join()

    print('Finish crawling products')
