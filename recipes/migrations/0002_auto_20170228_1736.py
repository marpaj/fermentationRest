# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 16:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredienttested',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='ingredienttested',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='ingredienttested',
            name='type',
        ),
        migrations.RemoveField(
            model_name='ingredienttested',
            name='units',
        ),
    ]
