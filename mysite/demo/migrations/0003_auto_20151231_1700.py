# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-31 09:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0002_web'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='money',
            field=models.FloatField(verbose_name='\u4e2d\u6807\u91d1\u989d'),
        ),
    ]
