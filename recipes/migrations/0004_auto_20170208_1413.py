# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-08 13:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20170207_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direction',
            name='description',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='direction',
            name='title',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
