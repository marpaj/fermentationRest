# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-07 12:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direction',
            name='description',
            field=models.CharField(max_length=400, null=True),
        ),
    ]