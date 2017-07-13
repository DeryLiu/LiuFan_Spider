# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u54c1\u7c7b')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u5546\u54c1')),
                ('url', models.URLField(verbose_name='\u94fe\u63a5')),
                ('images', models.TextField(verbose_name='\u56fe\u7247')),
                ('brand', models.CharField(max_length=100, verbose_name='\u54c1\u724c')),
                ('star', models.FloatField(null=True, verbose_name='\u8bc4\u5206')),
                ('category', models.ForeignKey(to='amazon.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('main_rank', models.IntegerField(verbose_name='\u6392\u540d')),
                ('other_ranks', models.CharField(max_length=200, verbose_name='\u5176\u4ed6\u6392\u540d')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('product', models.ForeignKey(verbose_name='\u4ea7\u54c1', to='amazon.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u5356\u5bb6')),
                ('url', models.URLField(verbose_name='\u94fe\u63a5')),
                ('products', models.ManyToManyField(related_name='sellers', verbose_name='\u4ea7\u54c1', to='amazon.Product')),
            ],
        ),
    ]
