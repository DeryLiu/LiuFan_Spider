#!/usr/bin/python
# coding=utf8
from gevent import monkey; monkey.patch_all()
import gevent
import os
import re
import time
import urllib
import urlparse
import configparser
import simplejson as json
from simplejson import JSONDecodeError
from spider import Spider
from spider import log_error
from spider import get_now

__author__ = 'Alex Yu'
__version__ = '0.1.0'


class EbaySpider(Spider):

    category_max_display_count = 10000

    def __init__(self, config_file=None):
        self.product_out_file = None

        # product_url information regulars
        self.category_key_high_low_page = set()
        self.product_id_reg = None
        self.product_url_reg = None
        self.product_name_reg = None
        self.product_brand_reg = None
        self.product_description_reg = None
        self.product_price_reg = None
        self.product_shipping_reg = None
        self.product_currency_reg = None
        self.product_seller_reg = None
        self.product_category_breads_reg = None
        self.product_category_id_reg = None
        self.product_category_reg = None
        self.product_keyword_reg = None
        self.product_isbn_reg = None
        self.product_weight_reg = None
        self.product_weight_class_reg = None
        self.product_width_reg = None
        self.product_length_reg = None
        self.product_height_reg = None
        self.product_length_class_reg = None
        self.product_ean_reg = None
        self.product_mpn_reg = None
        self.product_jan_reg = None
        self.product_detail_reg = None
        self.product_registered_land_reg = None
        self.product_location_reg = None
        self.product_order_reg = None
        self.product_review_reg = None
        self.product_images_reg = None
        self.product_attributes_reg = None
        self.product_attribute_select_reg = None
        self.product_attribute_img_arr_reg = None
        self.product_attribute_menu_item_map_reg = None
        self.product_attribute_menu_item_pic_index_map = None
        self.html_paths = None
        super(EbaySpider, self).__init__(config_file)

    def init_result_path(self, name='spider'):
        name = 'ebay'
        super(EbaySpider, self).init_result_path(name)

    @log_error
    def load_configs(self, path):
        super(EbaySpider, self).load_configs(path=path)
        conf = configparser.ConfigParser()
        conf.read(path)

        self.product_out_file = conf.get('files', 'product_out_file')

        # Parse product_url info regulars
        self.product_id_reg = re.compile(conf.get('product_info_regulars', 'product_id_reg'))
        self.product_url_reg = re.compile(conf.get('product_info_regulars', 'product_url_reg'))
        self.product_name_reg = re.compile(conf.get('product_info_regulars', 'product_name_reg'))
        self.product_brand_reg = re.compile(conf.get('product_info_regulars', 'product_brand_reg'))
        self.product_description_reg = re.compile(conf.get('product_info_regulars', 'product_description_reg'))
        self.product_price_reg = re.compile(conf.get('product_info_regulars', 'product_price_reg'))
        self.product_shipping_reg = re.compile(conf.get('product_info_regulars', 'product_shipping_reg'))
        self.product_currency_reg = re.compile(conf.get('product_info_regulars', 'product_currency_reg'))
        self.product_seller_reg = re.compile(conf.get('product_info_regulars', 'product_seller_reg'))
        self.product_category_breads_reg = re.compile(conf.get('product_info_regulars', 'product_category_breads_reg'))
        self.product_category_id_reg = re.compile(conf.get('product_info_regulars', 'product_category_id_reg'))
        self.product_category_reg = re.compile(conf.get('product_info_regulars', 'product_category_reg'))
        self.product_keyword_reg = re.compile(conf.get('product_info_regulars', 'product_keyword_reg'))
        self.product_isbn_reg = re.compile(conf.get('product_info_regulars', 'product_isbn_reg'))
        self.product_weight_reg = re.compile(conf.get('product_info_regulars', 'product_weight_reg'))
        self.product_weight_class_reg = re.compile(conf.get('product_info_regulars', 'product_weight_class_reg'))
        self.product_width_reg = re.compile(conf.get('product_info_regulars', 'product_width_reg'))
        self.product_height_reg = re.compile(conf.get('product_info_regulars', 'product_height_reg'))
        self.product_length_reg = re.compile(conf.get('product_info_regulars', 'product_length_reg'))
        self.product_length_class_reg = re.compile(conf.get('product_info_regulars', 'product_length_class_reg'))
        self.product_ean_reg = re.compile(conf.get('product_info_regulars', 'product_ean_reg'))
        self.product_mpn_reg = re.compile(conf.get('product_info_regulars', 'product_mpn_reg'))
        self.product_jan_reg = re.compile(conf.get('product_info_regulars', 'product_jan_reg'))
        self.product_detail_reg = re.compile(conf.get('product_info_regulars', 'product_detail_reg'))
        self.product_registered_land_reg = re.compile(conf.get('product_info_regulars', 'product_registered_land_reg'))
        self.product_location_reg = re.compile(conf.get('product_info_regulars', 'product_location_reg'))
        self.product_order_reg = re.compile(conf.get('product_info_regulars', 'product_order_reg'))
        self.product_review_reg = re.compile(conf.get('product_info_regulars', 'product_review_reg'))
        self.product_images_reg = re.compile(conf.get('product_info_regulars', 'product_images_reg'))
        self.product_attributes_reg = re.compile(conf.get('product_info_regulars', 'product_attributes_reg'))
        self.product_attribute_select_reg = re.compile(conf.get('product_info_regulars', 'product_attribute_select_reg'))
        self.product_attribute_img_arr_reg = re.compile(conf.get('product_info_regulars', 'product_attribute_img_arr_reg'))
        self.product_attribute_menu_item_map_reg = re.compile(conf.get('product_info_regulars', 'product_attribute_menu_item_map_reg'))
        self.product_attribute_menu_item_pic_index_map = re.compile(conf.get('product_info_regulars', 'product_attribute_menu_item_pic_index_map'))

    @log_error
    def update_category_urls(self):
        html = self.get_url_html(self.category_list_url)
        empty_keys = len(self.category_keys) == 0
        if empty_keys:
            pass
        else:
            a_tags = self.category_a_tag_reg.findall(html)
            for a_tag in a_tags:
                href = a_tag[0]
                category = self.category_reg.search(href).groupdict()
                key, value = category['key'], category['value']
                url = self.make_page_url(key, value)
                if key in self.category_keys:
                    leaf_urls = self.get_leaf_category_urls(url)
                    if leaf_urls:
                        self.category_urls.update(leaf_urls)
                    else:
                        self.category_urls.add(url)

    @log_error
    def get_leaf_category_urls(self, url):
        leaf_urls = set()
        urls = set()
        urls.add(url)
        while urls:
            u = urls.pop()
            html = self.get_url_html(u)
            if 'leafsiblings' not in html:
                leaf_a_tags = self.category_leaf_reg.findall(html)
                for a_tag in leaf_a_tags:
                    href = a_tag[0]
                    urls.add(href)
                    leaf_urls.add(href)
            else:
                leaf_urls.add(u)
        return leaf_urls

    @log_error
    def get_list_page_next_url(self, html, **kwargs):
        """
        提取页面下的下一页分页地址
        :param kwargs:
        :param html:
        :return:
        """
        # cur_url = u'http://www.ebay.com/sch/xzpbFNlGoDqUVtEocc/162916/i.html'
        data = {}
        curl_url = kwargs.get('cur_url')
        low_price = kwargs.get('low_price', '')
        high_price = kwargs.get('high_price', '')
        page = kwargs.get('page', 1)
        temp_url = re.sub(r'bn_\d+/', '', curl_url)
        total = self.get_category_product_total(html)
        if total > 0 and curl_url is not None:
            max_page = int(self.category_max_display_count / self.category_per_page)
            last_page = int((total - 1) / self.category_per_page) + 1
            next_page = page + 1
            if next_page < min(last_page, max_page):
                data.update({
                    'LH_ItemCondition': 3,
                    'LH_BIN': 1,
                    'LH_RPA': 1,
                    'LH_LocatedIn': 45,
                    'rt': 'nc',
                    '_mPrRngCbx': '1',
                    '_udlo': low_price,
                    '_udhi': high_price,
                    '_pgn': next_page,
                    '_ipg': self.category_per_page,
                    '_skc': page * self.category_per_page
                })
                return temp_url + '?' + urllib.urlencode(data)

    @log_error
    def work_out_url(self, base_url, low, high, page):
        url = base_url + '?'
        data = {
            'LH_ItemCondition': 3,
            'LH_BIN': 1,
            'LH_RPA': 1,
            'LH_LocatedIn': 45,
            '_mPrRngCbx': 1,
            '_dmd': 1,
            '_udlo': low or '',
            '_udhi': high or '',
            '_pgn': page or '',
            '_ipg': self.category_per_page
        }
        url += urllib.urlencode(data)
        return url

    @log_error
    def work_out_section(self, url, low, high, page, last_total, html):
        with open(self.result_path + self.category_urls_file, 'a') as f:
            f.write(url + '\n')
        self.update_product_urls(html)
        section = None
        # 剩下的总数小于category_max_display_count才进行判断是否一次可以取完所有的产品
        if self.category_max_display_count > last_total > 0 != high:
            return high, 0.0
        elif page > 1 or last_total < 1 or high > 1000000:
            pass
        else:
            section = high, round(high * 1.5, 2)  # 取下一个价格区间
        base_url = url.split('?')[0]
        next_url = self.get_list_page_next_url(html, cur_url=base_url, low_price=low, high_price=high, page=page)
        if next_url is not None:
            key, _ = self.get_category_key_value(next_url)
            key_high_low_page = (key, high, low, page + 1)
            if key_high_low_page not in self.category_key_high_low_page:
                self.category_urls.add(next_url)
                self.category_key_high_low_page.add(key_high_low_page)
        return section

    # @log_error
    def update_product_urls(self, html):
        """
        从html中提取需要的信息，写入self.product_keys
        只记录key
        :param html:
        :return:
        """
        product_a_tags = self.product_a_tag_reg.findall(html)
        print 'find %s products' % len(product_a_tags)
        for a_tag in product_a_tags:
            product_dict = self.product_reg.search(a_tag).groupdict()
            if self.update == 1 or product_dict['key'] not in self.product_keys:
                self.product_keys.add(product_dict['key'])
                with open(self.result_path + self.product_urls_file, 'a') as f:
                    f.write(self.make_product_url(product_dict['key'], product_dict['value']) + '\n')

    @log_error
    def update_category_pager_urls(self):
        """
        根据key,value和page生成分页链接,
        根据获取到的html获得产品链接
        :return:
        """
        # 该循环用于处理不同的分类链接
        while self.category_urls:
            url = self.category_urls.pop()
            base_url = url.split('?')[0]
            low, high, page = 0.0, 0.0, 1
            last_total = 0
            result = urlparse.urlparse(url)
            d = urlparse.parse_qs(result.query, True)
            if '_udlo' in d:
                low = float(d['_udlo'][0] or 0)
            if '_udhi' in d:
                high = float(d['_udhi'][0] or 0)
            if '_pgn' in d:
                page = int(d['_pgn'][0] or 1)
            # 该循环用于处理价格区间问题
            while True:
                format_url = self.work_out_url(base_url, low, high, page)
                if format_url is None:
                    break
                # format_url = cate_url
                html = self.get_url_html(format_url)
                total = self.get_category_product_total(html)
                if total > self.category_max_display_count:
                    # 修改合适的价格区间
                    if low == high == 0:                # 第一次进入，商品数量超出上限，第一次划分区间
                        high = 50.0
                        last_total = total
                    elif low != 0 and high == 0:        # 尝试将剩下的所有产品作为一个区间失败，修改区间，重试
                        high = round(low * 2, 2)
                        last_total = total
                    elif high - low < 0.02:             # 区间不能有效缩小分类数量了，只能放弃继续缩小区间
                        last_total -= total
                        section = self.work_out_section(format_url, low, high, page, last_total, html)
                        if section is None:
                            break
                        else:
                            low, high = section
                    else:
                        high = round((high + low) / 2, 2)
                        while high <= low:
                            high += 1.0
                else:
                    last_total -= total
                    section = self.work_out_section(format_url, low,  high, page, last_total, html)
                    if section is None:
                        break
                    else:
                        low, high = section

    def get_category_product_total(self, html):
        match = self.category_list_count_reg.search(html)
        return match and int((match.group(2) or match.group(3) or '0').replace(',', '')) or 0

    @log_error
    def retrieve_product_id(self, html):
        if self.product_id_reg.pattern != '':
            m = self.product_id_reg.search(html)
            product_id = m and m.group(1) or ''
            return self.clean_html_tag(product_id)
        return ''

    @log_error
    def retrieve_product_url(self, html):
        if self.product_url_reg.pattern != '':
            m = self.product_url_reg.search(html)
            product_url = m and m.group(1) or ''
            if product_url:
                return self.clean_html_tag(product_url)
        reg = re.compile('<div id="ebay-scShare-div" [^>]*data-cate_url="([^"]+)" [^>]*>')
        m = reg.search(html)
        product_url = m and m.group(1) or ''
        return self.clean_html_tag(product_url)

    @log_error
    def retrieve_product_name(self, html):
        if self.product_name_reg.pattern != '':
            m = self.product_name_reg.search(html)
            name = m and m.group(1) or ''
            return self.clean_html_tag(name)
        return ''

    @log_error
    def retrieve_product_brand(self, html):
        if self.product_brand_reg.pattern != '':
            m = self.product_brand_reg.search(html)
            brand = m and m.group(1) or ''
            return self.clean_html_tag(brand)
        return ''

    @log_error
    def retrieve_product_detail(self, html):
        if self.product_detail_reg.pattern != '':
            items = self.product_detail_reg.findall(html)
            return {k.strip().strip(':'): self.html_reg.sub(r'', v).strip() for k, v in items}
        return {}

    @log_error
    def retrieve_product_description(self, html):
        if self.product_description_reg.pattern != '':
            m = self.product_description_reg.search(html)
            desc = m and m.group(1) or ''
            return self.clean_html_tag(desc)
        return ''

    @log_error
    def retrieve_product_price(self, html):
        if self.product_price_reg.pattern != '':
            m = self.product_price_reg.search(html)
            price = m and m.group(1) or ''
            return self.clean_html_tag(price)
        return ''

    @log_error
    def retrieve_product_shipping(self, html):
        if self.product_shipping_reg.pattern != '':
            m = self.product_shipping_reg.search(html)
            shipping = m and m.group(1) or '0'
            if shipping == 'FREE':
                shipping = '0'
            return self.clean_html_tag(shipping)
        return '0'

    @log_error
    def retrieve_product_currency(self, html):
        if self.product_currency_reg.pattern != '':
            m = self.product_currency_reg.search(html)
            currency = m and m.group(1) or ''
            if not currency:
                reg = re.compile('<span class="notranslate" id="prcIsum"[^>]*>([^<]+?)\d+\.\d*</span>')
                m_cur = reg.search(html)
                currency = m_cur and m_cur.group(1) or ''
                currency = currency.strip()
                if currency.strip() == 'US $':
                    currency = 'USD'
            return self.clean_html_tag(currency)
        return ''

    @log_error
    def retrieve_product_seller(self, html):
        if self.product_seller_reg.pattern != '':
            m = self.product_seller_reg.search(html)
            seller = m and m.group(1) or ''
            return self.clean_html_tag(seller)
        return ''

    @log_error
    def retrieve_product_category_breads(self, html):
        # html = self.space_reg.sub(r'', html)      # 非常影响性能
        if self.product_category_breads_reg.pattern != '':
            m = self.product_category_breads_reg.search(html)
            breads = m and m.group(1) or ''
            return self.clean_html_tag(breads)
        return ''

    @log_error
    def retrieve_product_category_ids(self, html):
        if self.product_category_breads_reg.pattern != '':
            m = self.product_category_breads_reg.search(html)
            if m and len(m.groups()) >= 1:
                html = m.groups()[-1]
                if self.product_category_id_reg.pattern != '':
                    ids = self.product_category_id_reg.findall(html)
                    return '>'.join(ids)
        return ''

    @log_error
    def retrieve_product_keyword(self, html):
        if self.product_keyword_reg.pattern != '':
            m = self.product_keyword_reg.search(html)
            keyword = m and m.group(1) or ''
            return self.clean_html_tag(keyword)
        return ''

    @log_error
    def retrieve_product_isbn(self, html):
        if self.product_isbn_reg.pattern != '':
            m = self.product_isbn_reg.search(html)
            isbn = m and m.group(1) or ''
            return self.clean_html_tag(isbn)
        return ''

    @log_error
    def retrieve_product_ean(self, html):
        if self.product_ean_reg.pattern != '':
            m = self.product_ean_reg.search(html)
            ean = m and m.group(1) or ''
            return self.clean_html_tag(ean)
        return ''

    @log_error
    def retrieve_product_mpn(self, html):
        if self.product_mpn_reg.pattern != '':
            m = self.product_mpn_reg.search(html)
            mpn = m and m.group(1) or ''
            return self.clean_html_tag(mpn)
        return ''

    @log_error
    def retrieve_product_jan(self, html):
        if self.product_jan_reg.pattern != '':
            m = self.product_jan_reg.search(html)
            jan = m and m.group(1) or ''
            return self.clean_html_tag(jan)
        return ''

    @log_error
    def retrieve_product_weight(self, html):
        if self.product_weight_reg.pattern != '':
            m = self.product_weight_reg.search(html)
            weight = m and m.group(1) or '0.0000'
            return self.clean_html_tag(weight)
        return '0.0000'

    @log_error
    def retrieve_product_weight_class(self, html):
        if self.product_weight_class_reg.pattern != '':
            m = self.product_weight_class_reg.search(html)
            weight_class = m and m.group(1) or 'kg'
            return self.clean_html_tag(weight_class)
        return 'kg'

    @log_error
    def retrieve_product_height(self, html):
        if self.product_height_reg.pattern != '':
            m = self.product_height_reg.search(html)
            height = m and m.group(1) or '0.0000'
            return self.clean_html_tag(height)
        return '0.0000'

    @log_error
    def retrieve_product_width(self, html):
        if self.product_width_reg.pattern != '':
            m = self.product_width_reg.search(html)
            width = m and m.group(1) or '0.0000'
            return self.clean_html_tag(width)
        return '0.0000'

    @log_error
    def retrieve_product_length(self, html):
        if self.product_length_reg.pattern != '':
            m = self.product_length_reg.search(html)
            length = m and m.group(1) or '0.0000'
            return self.clean_html_tag(length)
        return '0.0000'

    @log_error
    def retrieve_product_length_class(self, html):
        if self.product_length_class_reg.pattern != '':
            m = self.product_length_class_reg.search(html)
            length_class = m and m.group(1) or 'cm'
            return self.clean_html_tag(length_class)
        return 'cm'

    @log_error
    def retrieve_product_registered_land(self, html):
        if self.product_registered_land_reg.pattern != '':
            m = self.product_registered_land_reg.search(html)
            land = m and m.group(1) or ''
            return self.clean_html_tag(land)
        return ''

    @log_error
    def retrieve_product_location(self, html):
        if self.product_location_reg.pattern != '':
            m = self.product_location_reg.search(html)
            location = m and m.group(1) or ''
            if not location:
                reg = re.compile('<div class="u-flL lable">Item location:</div>[^<]*<div class="u-flL">([^<]+)</div>')
                m_loc = reg.search(html)
                if m_loc:
                    location = m_loc.group(1)
            return location
        return ''

    @log_error
    def retrieve_product_order(self, html):
        if self.product_order_reg.pattern != '':
            m = self.product_order_reg.search(html)
            order = m and m.group(1) or '0'
            return self.clean_html_tag(order)
        return '0'

    @log_error
    def retrieve_product_review(self, html):
        if self.product_review_reg.pattern != '':
            m = self.product_review_reg.search(html)
            review = m and m.group(1) or '0'
            return self.clean_html_tag(review)
        return '0'

    @log_error
    def retrieve_product_images(self, html):
        if self.product_images_reg.pattern != '':
            image_urls = self.product_images_reg.findall(html)
            image_urls = list(set(image_urls))
            if not image_urls:
                reg = re.compile('<img[^>]* id="icImg"[^>]* src="([^"]+)" [^>]*>')
                image_urls = set(reg.findall(html))
            return [
                url.replace('\\u002F', '/').replace('s-l64', 's-l1600').replace('s-l300', 's-l1600').replace('s-l300', 's-l1600').replace('s-l500', 's-l1600') for url in image_urls]
        return []

    @log_error
    def retrieve_product_attribute_images(self, html):
        image_map = {}
        img_arr_match = self.product_attribute_img_arr_reg.search(html)
        menu_item_match = self.product_attribute_menu_item_map_reg.search(html)
        menu_item_pic_index_match = self.product_attribute_menu_item_pic_index_map.search(html)
        if img_arr_match and menu_item_match and menu_item_pic_index_match:
            try:
                img_arr = json.loads(img_arr_match.group(1))
                menu_item_map = json.loads(menu_item_match.group(1))
                menu_item_pic_index = json.loads(menu_item_pic_index_match.group(1))
            except JSONDecodeError as e:
                print '%s\t%s\t%s' % (get_now(), self.retrieve_product_url(html), e.message)
                menu_item_pic_index = {}
                menu_item_map = {}
                img_arr = {}
            for key, data in menu_item_pic_index.iteritems():
                menu_item = menu_item_map.get(key)
                if menu_item:
                    matching_variation_ids = menu_item.get('matchingVariationIds', [])
                    for vid in matching_variation_ids:
                        vid = str(vid)
                        if vid not in image_map:
                            image_map[vid] = []
                        for d in data:
                            img = img_arr[d].get('displayImgUrl')
                            image_map[vid].append(img)
        return image_map

    def retrieve_product_attributes(self, html):
        if self.product_attributes_reg.pattern != '':
            attributes = []
            m_attr = self.product_attributes_reg.search(html)
            if m_attr:
                try:
                    item_variations_map = json.loads(m_attr.group(1), encoding='UTF-8')
                except JSONDecodeError as e:
                    print '%s\t%s\t%s' % (get_now(), self.retrieve_product_url(html), e.message)
                    item_variations_map = {}
                image_map = self.retrieve_product_attribute_images(html)
                attr_map = {item[0]: item[1] for item in self.product_attribute_select_reg.findall(html)}
                product_id = self.retrieve_product_id(html)
                for variation, data in item_variations_map.iteritems():
                    attr = data.get('traitValuesMap')
                    for k, v in attr.iteritems():
                        attr[k] = attr_map[str(v)]
                    m_price = self.number_reg.search(data.get('price'))
                    if m_price is None or not m_price.group():
                        continue
                    attributes.append({
                        'variation_id': '%s_%s' % (product_id, variation),
                        'price': m_price.group(),
                        'image': image_map.get(variation, []),
                        'attributes': data.get('traitValuesMap'),
                        'dictory': ','.join([key for key in attr]),
                        'reviews': 0,
                        'quantity': data.get('quantity')
                    })
            return attributes
        return []

    @log_error
    def retrieve_product_category_id(self, html):
        if self.product_category_breads_reg.pattern != '':
            breads = self.product_category_breads_reg.findall(html)
            if breads:
                bread = breads[-1]
                m = self.product_category_reg.search(bread)
                return m and m.group(1) or ''
        return ''

    @log_error
    def retrieve_product_upc(self, html):
        return ''

    @log_error
    def retrieve_product_key_attribute(self, html):
        return ''

    @log_error
    def retrieve_product_info(self, html):
        values = super(EbaySpider, self).retrieve_product_info(html)
        values.update({
            'product_id': self.retrieve_product_id(html),
            'cate_url': self.retrieve_product_url(html),
            'name': self.retrieve_product_name(html),
            'brand': self.retrieve_product_brand(html),
            'detail': self.retrieve_product_detail(html),
            'keyword': self.retrieve_product_keyword(html),
            'key_attribute': self.retrieve_product_key_attribute(html),
            'description': self.retrieve_product_description(html),
            'price': self.retrieve_product_price(html),
            'shipping': self.retrieve_product_shipping(html),
            'currency': self.retrieve_product_currency(html),
            'seller_id': self.retrieve_product_seller(html),
            'cate_url': self.retrieve_product_category_breads(html),
            'isbn': self.retrieve_product_isbn(html),
            'ean': self.retrieve_product_ean(html),
            'mpn': self.retrieve_product_mpn(html),
            'jan': self.retrieve_product_jan(html),
            'weight': self.retrieve_product_weight(html),
            'weight_class': self.retrieve_product_weight_class(html),
            'height': self.retrieve_product_height(html),
            'width': self.retrieve_product_width(html),
            'length': self.retrieve_product_length(html),
            'length_class': self.retrieve_product_length_class(html),
            'registered_land': self.retrieve_product_registered_land(html),
            'location': self.retrieve_product_location(html),
            'orders': self.retrieve_product_order(html),
            'reviews': self.retrieve_product_review(html),
            'image': self.retrieve_product_images(html),
            'upc': self.retrieve_product_upc(html),
            'attributes': self.retrieve_product_attributes(html),
            'category_id_path': self.retrieve_product_category_ids(html)
        })
        return self.check_data(values)

    @log_error
    def check_data(self, values):
        values['category_id'] = values['category_id_path'].split('>')[-1]
        values['key_name'] = values['cate_url'].split('>')[0]
        if len(values['attributes']) < 1:
            attributes = {
                'price': values['price'],
                'variation_id': '%s_%s' % (values['product_id'], values['product_id']),
                'dictory': '',
                'attributes': {},
                'image': values['image'],
                'quantity': values['orders']
            }
            values['attributes'] = [attributes]

        for k, v in values['detail'].items():
            k = k.lower()
            v = v.lower()
            if k in values:
                if k in ['width', 'height', 'length', 'weight']:
                    num_reg = re.compile(r'(^\d+\.?\d*)')
                    cls_reg = re.compile(r'([a-zA-Z]+$)')
                    m = num_reg.search(v)
                    if m:
                        values[k] = m.group(1) or '0.0000'
                    m = cls_reg.search(v)
                    if m:
                        if k == 'weight':
                            values['weight_class'] = m.group(1) or 'cm'
                        else:
                            values['length_class'] = m.group(1) or 'cm'

        return values['cate_url'] and values['price'] and values or None

    @log_error
    def load_html_paths(self):
        html_path = self.result_path + 'html/'
        if not os.path.exists(html_path):
            os.makedirs(html_path)
        print 'Get html from file: %s' % html_path
        self.html_paths = [html_path + html_file for html_file in os.listdir(html_path) if os.path.isfile(html_path + html_file) and html_file.endswith('.html')]

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
                    'cate_url': url
                })
                html = self.get_url_html(url)
                if html is not None:
                    if self.download_file:
                        html_path = self.result_path + 'html/'
                        if not os.path.exists(html_path):
                            os.makedirs(html_path)
                        html_file_path = html_path + '%s.html' % key
                        with open(html_file_path, 'wt') as f:
                            f.write(html)
                    info = self.retrieve_product_info(html)
                    if info is not None:
                        values.update(info)
                        product_file = self.result_path + self.product_out_file
                        with open(product_file, 'a') as f:
                            f.writelines(json.dumps(values) + '\n')

    @log_error
    def release_category_men(self):
        del self.category_key_high_low_page
        return super(EbaySpider, self).release_category_men()

    def run(self, workers=8, download=True, get_urls=True, crawl_products=True, count=100000):
        """
        启动爬虫
        :param workers: 设置gevent并发数
        :param download: 设置是否下载产品html文件
        :param get_urls: 设置是否获取分类和产品链接
        :param crawl_products: 设置是否抓产品信息
        :param count: 设置每次抓产品信息时最大的个数
        :return:
        """
        self.init_result_path()
        self.download_file = download
        if get_urls:
            self.update_category_urls()
            print 'Leaf cate_url urls：%s' % len(self.category_urls)
            gevent.joinall([gevent.spawn(self.update_category_pager_urls) for _ in range(workers)])
            self.release_category_men()
        if crawl_products:
            product_count = 0
            product_file = self.result_path + self.product_out_file
            product_url_file = self.result_path + self.product_urls_file
            if os.path.exists(product_file):
                os.remove(product_file)
            if os.path.exists(product_url_file):
                with open(product_url_file) as product_urls:
                    for url in product_urls:
                        product_count += 1
                        if url.endswith('\n'):
                            url = url[:-1]
                        self.product_urls.add(url)
                        if product_count >= count:
                            print 'Crawl %s products' % len(self.product_urls)
                            product_count = 0
                            gevent.joinall([gevent.spawn(self.crawl_products) for _ in range(workers)])
                    else:
                        print 'Crawl the rest %s products' % len(self.product_urls)
                        gevent.joinall([gevent.spawn(self.crawl_products) for _ in range(workers)])


if __name__ == '__main__':
    spider = EbaySpider('ebay.conf')
    # spider.result_path = 'results/ebay/2016/1020/'
    # spider.load_html_paths()
    # gevent.joinall([gevent.spawn(spider.crawl_products_from_html_gevent) for _ in range(100)])
    spider.run(workers=100, download=True, get_urls=True, crawl_products=True)
