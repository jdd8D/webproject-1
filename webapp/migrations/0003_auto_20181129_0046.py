# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-11-28 23:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20181128_2354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='technology',
            name='image_url_c',
        ),
        migrations.RemoveField(
            model_name='technology',
            name='image_url_i',
        ),
        migrations.RemoveField(
            model_name='technology',
            name='image_url_l',
        ),
        migrations.RemoveField(
            model_name='technology',
            name='image_url_m',
        ),
        migrations.RemoveField(
            model_name='technology',
            name='image_url_r',
        ),
        migrations.AddField(
            model_name='technology',
            name='image',
            field=models.ImageField(default='technologies/default.jpg', null=True, upload_to='technologies/', verbose_name='url image'),
        ),
    ]
