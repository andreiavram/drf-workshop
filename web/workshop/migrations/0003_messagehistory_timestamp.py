# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-11 01:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0002_auto_20171110_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagehistory',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2017, 11, 11, 1, 2, 25, 395112, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
