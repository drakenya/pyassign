# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-07 19:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='khs_id_field',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='part',
            name='khs_title_field',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]