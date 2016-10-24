# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-20 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0013_auto_20161020_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricelistmodel',
            name='brand_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pricelistmodel',
            name='dealer_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pricelistmodel',
            name='model',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pricelistmodel',
            name='producer',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pricelistmodel',
            name='recomend_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pricelistmodel',
            name='rozn_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]