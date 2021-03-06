# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-14 23:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linkpearl_lodestone', '0004_auto_20151214_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='slug',
            field=models.CharField(default='no-slug', max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='server',
            name='slug',
            field=models.SlugField(default='no-slug', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='character',
            name='clan',
            field=models.IntegerField(choices=[(1, 'First'), (2, 'Second')]),
        ),
    ]
