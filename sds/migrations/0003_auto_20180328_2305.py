# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-29 05:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sds', '0002_auto_20170802_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoCaja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=40)),
            ],
        ),
        migrations.AlterField(
            model_name='operador',
            name='fecha_alta',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 28, 23, 5, 30, 148938)),
        ),
        migrations.AlterField(
            model_name='operador',
            name='fecha_baja',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 28, 23, 5, 30, 148978)),
        ),
    ]
