# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-11-28 22:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technology',
            name='need',
            field=models.ManyToManyField(blank=True, to='webapp.Need', verbose_name='besoin'),
        ),
        migrations.AlterField(
            model_name='technology',
            name='technotype',
            field=models.ManyToManyField(blank=True, to='webapp.Technotype', verbose_name='type de technologie'),
        ),
    ]
