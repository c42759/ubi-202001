# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-01-26 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urban_environment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alerts',
            name='latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='alerts',
            name='longitude',
            field=models.FloatField(default=0),
        ),
    ]
