# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-25 09:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_test_closed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='product',
        ),
    ]
