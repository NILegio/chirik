# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-09 20:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aas', '0005_auto_20171008_0859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentary',
            name='path',
        ),
    ]
