# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20170523_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hellspawn',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20)),
                ('name_pinyin', models.CharField(default='', max_length=128)),
                ('name_abbr', models.CharField(default='', max_length=10)),
                ('rarity', models.IntegerField(choices=[(1, 'SSR'), (2, 'SR'), (3, 'R'), (4, 'N')], default=4)),
                ('picture', models.CharField(blank=True, null=True, max_length=128)),
                ('icon', models.CharField(blank=True, null=True, max_length=128)),
                ('clue1', models.CharField(blank=True, null=True, max_length=30)),
                ('clue2', models.CharField(blank=True, null=True, max_length=30)),
            ],
        ),
    ]
