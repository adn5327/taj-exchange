# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-16 18:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0003_auto_20160412_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='security',
            name='sector',
            field=models.CharField(default='Unknown', max_length=25),
        ),
    ]