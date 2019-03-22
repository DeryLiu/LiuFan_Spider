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
                ('name', models.CharField(max_length=120)),
                ('url', models.URLField()),
                ('is_leaf', models.NullBooleanField()),
                ('status', models.CharField(default=b'done', max_length=10, choices=[(b'pending', b'Pending'), (b'done', b'Done'), (b'failed', b'Failed')])),
                ('product_total', models.IntegerField(null=True)),
                ('product_success', models.IntegerField(null=True)),
                ('product_failed', models.IntegerField(null=True)),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='dashboard.Category', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('url', models.URLField()),
                ('external_id', models.CharField(max_length=200)),
                ('server', models.CharField(max_length=60)),
                ('off_shelf', models.BooleanField(default=False)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(to='dashboard.Category', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('rate', models.CharField(max_length=1, choices=[(b'o', '\u4e00\u6b21'), (b'd', '\u6bcf\u5929'), (b'w', '\u6bcf\u5468'), (b'm', '\u6bcf\u6708')])),
                ('start_time', models.DateTimeField(auto_now=True)),
                ('task_type', models.CharField(max_length=10, choices=[(b'crawl', '\u6293\u53d6'), (b'update', '\u66f4\u65b0')])),
                ('category_keys', models.TextField(default=b'')),
                ('category_names', models.TextField(default=b'')),
                ('status', models.CharField(default=b'done', max_length=10, choices=[(b'pending', b'Pending'), (b'done', b'Done'), (b'failed', b'Failed')])),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=120, verbose_name='\u7ad9\u70b9')),
                ('url', models.URLField(verbose_name='\u5730\u5740')),
                ('spider_class', models.CharField(default=b'', max_length=20, verbose_name='\u722c\u866b\u7c7b\u540d', choices=[(b'ebay', b'Ebay\xe3\x80\x80Spider'), (b'amazon', b'Amazon Spider')])),
                ('logo', models.ImageField(upload_to=b'images/%Y/%m/%d', null=True, verbose_name='Logo', blank=True)),
                ('status', models.CharField(default=b'done', max_length=10, choices=[(b'pending', b'Pending'), (b'done', b'Done'), (b'failed', b'Failed')])),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='site',
            field=models.ForeignKey(to='dashboard.Website'),
        ),
        migrations.AddField(
            model_name='category',
            name='site',
            field=models.ForeignKey(to='dashboard.Website', null=True),
        ),
    ]
