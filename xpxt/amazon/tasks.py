# coding=utf-8
import os
from celery import shared_task, group, chord
from .spider.amazon_spider import AmazonSpider


def chars_utf8(chars):
    return isinstance(chars, str) and chars.decode('utf-8') or unicode(chars)


@shared_task
def hello(msg):
    print('#' * 80)
    print(msg)


@shared_task
def task_get_product_info(product_url, *args, **kwargs):
    pass


@shared_task
def task_get_top_100_products(url, *args, **kwargs):
    spider = AmazonSpider(os.path.join(os.getcwd(), 'amazon/spider/amazon.conf'))
    product_urls = spider.get_top_100(url)
    chord(task_get_product_info.s(url, *args, **kwargs) for url in product_urls)(hello.s())


@shared_task
def task_split_category_urls(category_urls, *args, **kwargs):
    if isinstance(category_urls, list):
        group(task_get_top_100_products.s(cat, *args, **kwargs) for cat in category_urls).delay()


@shared_task
def task_get_leaf_categories(category_url):
    spider = AmazonSpider(os.path.join(os.getcwd(), 'amazon/spider/amazon.conf'))
    return spider.get_leaf_categories(category_url)


@shared_task
def task_get_top_products(category_url, *args, **kwargs):
    spider = AmazonSpider(os.path.join(os.getcwd(), 'amazon/spider/amazon.conf'))
    child_cats = spider.get_child_categories(category_url)
    group([chord(task_get_leaf_categories.s(chars_utf8(cat)))(task_split_category_urls.s(*args, **kwargs)) for cat in child_cats])
