# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comment_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='user',
            field=models.ForeignKey(related_name='articles', to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]
