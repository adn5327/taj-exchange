# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-11 06:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0009_auto_20160411_0141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posessions',
            old_name='account',
            new_name='pos_account',
        ),
        migrations.RenameField(
            model_name='posessions',
            old_name='security',
            new_name='pos_security',
        ),
        migrations.RenameField(
            model_name='trade',
            old_name='security',
            new_name='trade_security',
        ),
        migrations.AlterUniqueTogether(
            name='posessions',
            unique_together=set([('pos_account', 'pos_security')]),
        ),
    ]