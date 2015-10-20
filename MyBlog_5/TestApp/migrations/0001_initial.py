# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('name', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('content_body', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('version', models.IntegerField(default=0)),
            ],
        ),
    ]
