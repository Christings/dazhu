# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-02 10:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ip_filter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ip',
            name='body',
            field=models.CharField(max_length=20),
        ),
    ]
