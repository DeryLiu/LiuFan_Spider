# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '\u54c1\u7c7b', 'verbose_name_plural': '\u54c1\u7c7b'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': '\u4ea7\u54c1', 'verbose_name_plural': '\u4ea7\u54c1'},
        ),
        migrations.AlterModelOptions(
            name='rank',
            options={'verbose_name': '\u6392\u540d', 'verbose_name_plural': '\u6392\u540d'},
        ),
        migrations.AlterModelOptions(
            name='seller',
            options={'verbose_name': '\u5356\u5bb6', 'verbose_name_plural': '\u5356\u5bb6'},
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(verbose_name='\u54c1\u7c7b', to='amazon.Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, verbose_name='\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='rank',
            name='main_rank',
            field=models.IntegerField(verbose_name='\u4e3b\u6392\u540d'),
        ),
        migrations.AlterField(
            model_name='rank',
            name='other_ranks',
            field=models.TextField(verbose_name='\u5176\u4ed6\u6392\u540d'),
        ),
    ]
