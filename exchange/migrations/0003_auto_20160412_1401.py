# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-12 19:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0002_auto_20160412_1357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='account_orders',
        ),
        migrations.RemoveField(
            model_name='account',
            name='account_securities',
        ),
    ]
