# encoding=utf-8
from celery import chain
from django.conf import settings
from django.db import models, IntegrityError
from django.db.models import F
from django.utils.timezone import now, timedelta

SPIDER_CHOICES = (
    ('ebay', 'Ebay　Spider'),
    ('amazon', 'Amazon Spider')
)

STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('done', 'Done'),
    ('failed', 'Failed')
)


class Website(models.Model):
    name = models.CharField(verbose_name=u'站点', max_length=120, unique=True, null=False)
    url = models.URLField(verbose_name=u'地址', null=False)
    spider_class = models.CharField(verbose_name=u'爬虫类名', max_length=20, default='', choices=SPIDER_CHOICES)
    logo = models.ImageField(verbose_name=u'Logo', upload_to='images/%Y/%m/%d', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='done')

    class Meta:
        app_label = 'dashboard'

    def __unicode__(self):
        return self.name

    def get_products(self, day=None, status=None):
        products = Product.objects.filter(category__site=self.pk)
        if day is not None:
            products = products.filter(update_time__gte=(now() - timedelta(day, 0)))
            if status == 'off':
                products = products.filter(off_shelf=True)
            elif status == 'new':
                products = products.filter(add_time=F('update_time'))
            elif status == 'update':
                products = products.filter(add_time__lt=F('update_time'))
        return products


class Category(models.Model):
    name = models.CharField(max_length=120)
    url = models.URLField()
    site = models.ForeignKey(Website, blank=False, null=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name="children", on_delete=models.CASCADE)
    is_leaf = models.NullBooleanField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='done')
    product_total = models.IntegerField(null=True)
    product_success = models.IntegerField(null=True)
    product_failed = models.IntegerField(null=True)

    class Meta:
        app_label = 'dashboard'

    def __unicode__(self):
        return self.name

    def get_name_path(self):
        path = self.name
        parent_category = self.parent
        while parent_category:
            path = parent_category.name + ' > ' + path
            parent_category = parent_category.parent
        return path

    def get_progress(self):
        return 100 if not self.product_total else int((self.product_success + self.product_failed) * 100 / self.product_total)


class Product(models.Model):
    name = models.CharField(max_length=120, null=False)
    url = models.URLField(max_length=200, null=False)
    external_id = models.CharField(max_length=200, null=False)
    category = models.ForeignKey(Category, blank=False, null=True, on_delete=models.CASCADE)
    server = models.CharField(max_length=60)
    off_shelf = models.BooleanField(default=False)
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'dashboard'

    def __unicode__(self):
        return self.name

    def get_status(self, day=0):
        if self.off_shelf:
            return u'已下架'
        if (self.update_time + timedelta(day, 0)).date() >= now().date():
            return u'更新' if self.update_time != self.add_time else u'新增'
        return u''


class Task(models.Model):
    name = models.CharField(max_length=100, unique=True)
    site = models.ForeignKey(Website, blank=False, null=False)
    rate = models.CharField(max_length=1, choices=(('o', u'一次'), ('d', u'每天'), ('w', u'每周'), ('m', u'每月')))
    start_time = models.DateTimeField(auto_now=True)
    task_type = models.CharField(max_length=10, choices=(('crawl', u'抓取'), ('update', u'更新')))
    category_keys = models.TextField(default='')
    category_names = models.TextField(default='')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='done')

    def __unicode__(self):
        return self.name
