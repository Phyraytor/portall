# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-10-02 09:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0003_auto_20181002_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='name',
            field=models.CharField(default='name', max_length=200),
            preserve_default=False,
        ),
    ]
