# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-20 08:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0012_auto_20161019_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricelistmodel',
            name='recomend_price',
            field=models.FloatField(null=True),
        ),
    ]
