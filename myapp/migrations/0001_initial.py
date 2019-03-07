# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-07 12:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Env',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('mark', models.CharField(max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MicService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('limits_cpu', models.IntegerField(default=1000)),
                ('limits_mem', models.IntegerField(default=2000)),
                ('requests_cpu', models.IntegerField(default=500)),
                ('requests_men', models.IntegerField(default=1000)),
                ('port', models.IntegerField(default=8080)),
                ('image', models.CharField(default='docker-hub.tools.huawei.com/clouddragon/euler', max_length=128)),
                ('replicas', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('Mark', models.CharField(max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=32)),
                ('mark', models.CharField(max_length=64, null=True)),
                ('MicService', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.MicService')),
            ],
        ),
        migrations.AddField(
            model_name='micservice',
            name='Service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Service'),
        ),
    ]