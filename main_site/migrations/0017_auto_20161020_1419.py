# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-20 11:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0016_auto_20161020_1156'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PriceListModel',
            new_name='Products',
        ),
        migrations.AlterModelTable(
            name='products',
            table='t_products',
        ),
    ]
