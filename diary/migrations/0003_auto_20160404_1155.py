# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-04 03:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0002_auto_20160404_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='timestamp',
            field=models.DateField(default=datetime.datetime(2016, 4, 4, 3, 55, 47, 926124, tzinfo=utc)),
        ),
    ]
