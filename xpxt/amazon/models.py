# coding=utf-8
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'品类')

    class Meta:
        verbose_name = u'品类'
        verbose_name_plural = u'品类'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'名称')
    category = models.ForeignKey(Category, verbose_name=u'品类', on_delete=models.CASCADE)
    url = models.URLField(verbose_name=u'链接')
    images = models.TextField(verbose_name=u'图片')
    brand = models.CharField(max_length=100, verbose_name=u'品牌')
    star = models.FloatField(verbose_name=u'评分', null=True)

    class Meta:
        verbose_name = u'产品'
        verbose_name_plural = u'产品'

    def __str__(self):
        return self.name

    def recent_rank(self):
        return self.rank_set.order_by('-create_date').first()
    recent_rank.short_description = u'最近排名'

    def seller_count(self):
        return self.sellers.count()
    seller_count.short_description = u'卖家数量'


class Rank(models.Model):
    product = models.ForeignKey(Product, verbose_name=u'产品')
    main_rank = models.IntegerField(verbose_name=u'主排名')
    other_ranks = models.TextField(verbose_name=u'其他排名')
    create_date = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name = u'排名'
        verbose_name_plural = u'排名'

    def __str__(self):
        return '#%s' % self.main_rank


class Seller(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'卖家')
    url = models.URLField(verbose_name=u'链接', unique=True)
    products = models.ManyToManyField(Product, verbose_name=u'产品', related_name='sellers')

    class Meta:
        verbose_name = u'卖家'
        verbose_name_plural = u'卖家'

    def __str__(self):
        return self.name
