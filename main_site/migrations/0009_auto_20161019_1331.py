# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-19 10:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0008_articles_banners_cart_catalog_constructpartners_constructpartnersit_constructpartnersitems_construct'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 't_categories',
            },
        ),
        migrations.CreateModel(
            name='PriceListModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('articul', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=255)),
                ('model', models.CharField(blank=True, max_length=255)),
                ('brend', models.CharField(blank=True, max_length=255)),
                ('producer', models.CharField(blank=True, max_length=255)),
                ('price_retail', models.FloatField(null=True)),
                ('price', models.FloatField()),
                ('dealer_price', models.FloatField(null=True)),
                ('balance', models.CharField(db_column='ostatok', max_length=255, null=True)),
                ('category_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_site.Categories')),
            ],
            options={
                'db_table': 't_price_list',
            },
        ),
        migrations.RenameModel(
            old_name='Document',
            new_name='Documents',
        ),
        migrations.AlterModelTable(
            name='documents',
            table='t_documents',
        ),
    ]
