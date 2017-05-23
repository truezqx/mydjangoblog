# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50, verbose_name='广告标题')),
                ('description', models.CharField(max_length=200, verbose_name='广告描述')),
                ('image_url', models.ImageField(upload_to='ad/%Y/%m', verbose_name='图片路径')),
                ('callback_url', models.URLField(blank=True, verbose_name='回调URL', null=True)),
                ('date_publish', models.DateField(auto_now_add=True, verbose_name='发布时间')),
                ('index', models.IntegerField(default=999, verbose_name='排列顺序（从小到大)')),
            ],
            options={
                'verbose_name_plural': '广告',
                'ordering': ['index', 'id'],
                'verbose_name': '广告',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('content', models.TextField(verbose_name='评论内容')),
                ('date_publish', models.DateField(auto_now_add=True, verbose_name='发布时间')),
                ('article', models.ForeignKey(blank=True, to='blog.Article', null=True, verbose_name='文章')),
                ('pid', models.ForeignKey(blank=True, to='blog.Comment', null=True, verbose_name='父级评论')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='用户')),
            ],
            options={
                'verbose_name_plural': '评论',
                'ordering': ['-date_publish'],
                'verbose_name': '评论',
            },
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('description', models.CharField(max_length=200, verbose_name='友情连接描述')),
                ('callback_url', models.URLField(verbose_name='url地址')),
                ('date_publish', models.DateField(auto_now_add=True, verbose_name='发布时间')),
                ('index', models.IntegerField(default=999, verbose_name='排列顺序（从小到大)')),
            ],
            options={
                'verbose_name_plural': '友情链接',
                'ordering': ['index', 'id'],
                'verbose_name': '友情链接',
            },
        ),
    ]
