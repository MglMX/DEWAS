# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=b'20')),
                ('description', models.TextField()),
                ('seller', models.CharField(max_length=b'30')),
                ('minimun_price', models.DecimalField(max_digits=b'7', decimal_places=b'2')),
                ('deadline', models.DateTimeField()),
                ('status', models.CharField(max_length=b'3')),
                ('last_bid', models.DecimalField(max_digits=b'7', decimal_places=b'2')),
                ('last_bider', models.CharField(max_length=b'30', blank=b'True')),
            ],
        ),
    ]
