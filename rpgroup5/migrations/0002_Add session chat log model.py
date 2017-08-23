# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-23 18:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpgroup5', '0001_add chapter model'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rp_group', models.CharField(max_length=32)),
                ('title', models.CharField(max_length=32)),
                ('content', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
