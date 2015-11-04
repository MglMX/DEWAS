# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TestApp', '0002_auction_desc_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='last_bid',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='auction',
            name='minimun_price',
            field=models.FloatField(),
        ),
    ]
