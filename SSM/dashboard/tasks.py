# encoding=utf-8
import os
import socket
import simplejson as json
from celery import shared_task, subtask, group
from django.db.models import F

from spider.ebay_spider import EbaySpider
from dashboard.models import Website, Category, Product, Task


@shared_task
def finish_init_category(pre_result, site_id):
    print(pre_result)
    print('Finish init category')
    print('#' * 80)
    Website.objects.filter(pk=site_id).update(status='done')


@shared_task(resultrepr_maxsize=1024*1024*100)
def group_categories(it, callback, site_id):
    print('Group categories')
    print(it)
    callback = subtask(callback)
    result = group(callback.clone((args, site_id)) for args in it)
    result.delay()


def make_category_tree(category_items, site_id):
    print('make category tree')
    category_map = dict()
    category_objs = set()
    site = Website.objects.get(pk=site_id)
    for item in category_items:
        url = item[1]
        parent_url = item[2]
        if parent_url is not None:
            parent_url = parent_url.strip()
            if parent_url in category_map:
                parent_cat = category_map[parent_url]
            else:
                parent_cat = Category.objects.filter(url=parent_url, site=site).first()
                category_map[parent_url] = parent_cat
        else:
            parent_cat = None
        defaults = {'url': url}
        cat, created = Category.objects.update_or_create(defaults, name=item[0], url=url, site=site, parent=parent_cat, is_leaf=item[3])
        category_objs.add(cat)
    return category_objs


@shared_task(resultrepr_maxsize=1024*1024*100, task_compression='bzip2')
def initial_categories(site_id):
    print('Initial categories: %s' % site_id)
    old_path = os.getcwd()
    os.chdir(os.path.join(old_path, 'dashboard/spider/'))
    spider = EbaySpider(os.path.join(os.getcwd(), 'ebay.conf'))
    os.chdir(old_path)
    print('After change dir')
    category_items = spider.get_top_categories()
    print(category_items)
    objs = make_category_tree(category_items, site_id)
    return list(set(obj.url for obj in objs))


@shared_task(resultrepr_maxsize=1024*1024*100, task_compression='bzip2')
def initial_category_children(category_url, site_id):
    print('Initial category children: %s')
    print(category_url)
    old_path = os.getcwd()
    os.chdir(os.path.join(old_path, 'dashboard/spider/'))
    spider = EbaySpider(os.path.join(os.getcwd(), 'ebay.conf'))
    os.chdir(old_path)
    category_items = spider.get_children_categories(category_url)
    make_category_tree(category_items, site_id)
    return 'success'


@shared_task(resultrepr_maxsize=1024*1024*100)
def group_tasks(it, callback):
    """
    这个方法是为了结合chain和group
    :param it:
    :param callback:
    :return:
    """
    callback = subtask(callback)
    result = group(callback.clone((args, )) for args in it)()
    return result


@shared_task(resultrepr_maxsize=1024*1024*100, time_limit=300, soft_time_limit=500)
def crawl_product_urls(category_url):
    """
    抓取产品链接
    :param category_url:
    :return:
    """
    print(u'产品链接%s' % category_url)
    old_path = os.getcwd()
    os.chdir(os.path.join(old_path, 'dashboard/spider/'))
    spider = EbaySpider(os.path.join(os.getcwd(), 'ebay.conf'))
    os.chdir(old_path)
    urls = spider.get_category_products(category_url)
    cat = Category.objects.filter(url=category_url, status='pending').first()
    if cat:
        urls = list(set(urls) - set(p.url for p in cat.product_set.all()))
        cat.product_total = len(urls)
        cat.product_success = 0
        cat.product_failed = 0
        cat.save()
    return list(urls)


@shared_task
def crawl_product_info(product_url, cat_url, out_file):
    """
    抓取产品详情
    :param product_url: 产品链接地址
    :param cat_url: 品类id
    :param out_file: 产品信息保存文件
    :return:
    """
    print(product_url)
    old_path = os.getcwd()
    os.chdir(os.path.join(old_path, 'dashboard/spider/'))
    spider = EbaySpider(os.path.join(os.getcwd(), 'ebay.conf'))
    os.chdir(old_path)
    cat = Category.objects.filter(url=cat_url).first()
    if cat:
        html = spider.get_url_html(product_url)
        if html is not None:
            info = spider.retrieve_product_info(html)
            if info is not None:
                defaults = {'name': info['name'], 'url': product_url, 'external_id': info['product_id'], 'category': cat, 'server': socket.gethostname()}
                Product.objects.update_or_create(defaults, url=product_url)
                data = json.dumps(info)
                with open(out_file, 'a') as f:
                    f.write('%s\n' % data)
                return 'success'
            else:
                # 产品信息抓取不到，判断为商品已下架
                Product.objects.filter(url=product_url).update(off_shelf=True)
            Category.objects.filter(url=cat_url).update(product_success=F('product_success') + 1)
        else:
            Category.objects.filter(url=cat_url).update(product_failed=F('product_failed') + 1)
    return


@shared_task
def finish_get_category_products(r, task_id):
    print(r)
    try:
        task = Task.objects.get(id=task_id)
        task.status = 'done'
        task.save()
        if task.task_type == 'crawl':
            Category.objects.filter(pk__in=task.category_keys.split(','), status='pending').update(status='done')
    except Task.DoesNotExist:
        print('Task %s not exist' % task_id)
    print('finish_get_category_products')


if __name__ == '__main__':
    pass
