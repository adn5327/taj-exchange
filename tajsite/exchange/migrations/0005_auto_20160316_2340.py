# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-17 04:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0004_auto_20160316_2339'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('SSN', 'id')]),
        ),
    ]
