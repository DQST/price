# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-19 12:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0011_auto_20161019_1434'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricelistmodel',
            old_name='price',
            new_name='recomend_price',
        ),
        migrations.RenameField(
            model_name='pricelistmodel',
            old_name='price_retail',
            new_name='rozn_price',
        ),
    ]
