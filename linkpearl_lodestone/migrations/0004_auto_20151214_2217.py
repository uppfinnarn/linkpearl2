# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-14 22:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linkpearl_lodestone', '0003_auto_20151214_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='clan_2',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
