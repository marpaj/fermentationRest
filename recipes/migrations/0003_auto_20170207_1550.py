# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-07 14:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20170207_1357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='direction',
            name='time',
        ),
        migrations.AlterField(
            model_name='directiontested',
            name='place',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='directiontested',
            name='time',
            field=models.CharField(max_length=60, null=True),
        ),
    ]