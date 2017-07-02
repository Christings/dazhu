# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-27 14:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_category_is_privite'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='last_update',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
