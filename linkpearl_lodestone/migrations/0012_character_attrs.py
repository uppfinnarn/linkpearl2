# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-15 15:54
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('linkpearl_lodestone', '0011_auto_20151215_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='attrs',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]
