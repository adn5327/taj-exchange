# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-11 06:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0010_auto_20160411_0146'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posessions',
            old_name='pos_account',
            new_name='account_id',
        ),
        migrations.RenameField(
            model_name='posessions',
            old_name='pos_security',
            new_name='security_id',
        ),
        migrations.RenameField(
            model_name='trade',
            old_name='trade_security',
            new_name='security_id',
        ),
        migrations.AlterUniqueTogether(
            name='posessions',
            unique_together=set([('account_id', 'security_id')]),
        ),
    ]
