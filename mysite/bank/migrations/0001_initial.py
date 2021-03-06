# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-11-12 01:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bankemploye',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serialNumber', models.CharField(blank=True, max_length=4, null=True)),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('subitem', models.CharField(blank=True, max_length=100, null=True)),
                ('drivingfactors', models.CharField(blank=True, max_length=100, null=True)),
                ('investigation', models.CharField(blank=True, max_length=100, null=True)),
                ('classificationNumber', models.CharField(blank=True, max_length=4, null=True)),
                ('score', models.CharField(blank=True, max_length=4, null=True)),
                ('dimensionalItems', models.CharField(blank=True, max_length=32, null=True)),
                ('remarks', models.CharField(blank=True, max_length=32, null=True)),
                ('a_analyse', models.CharField(blank=True, max_length=500, null=True)),
                ('b_analyse', models.CharField(blank=True, max_length=500, null=True)),
                ('c_analyse', models.CharField(blank=True, max_length=500, null=True)),
                ('d_analyse', models.CharField(blank=True, max_length=500, null=True)),
                ('e_analyse', models.CharField(blank=True, max_length=500, null=True)),
                ('a', models.IntegerField(default=0)),
                ('b', models.IntegerField(default=0)),
                ('c', models.IntegerField(default=0)),
                ('d', models.IntegerField(default=0)),
                ('e', models.IntegerField(default=0)),
                ('a_per', models.FloatField(default=0)),
                ('b_per', models.FloatField(default=0)),
                ('c_per', models.FloatField(default=0)),
                ('d_per', models.FloatField(default=0)),
                ('e_per', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Bankuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=10, null=True)),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('ask', models.CharField(blank=True, max_length=100, null=True)),
                ('reply', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=12, null=True)),
                ('email', models.CharField(blank=True, max_length=24, null=True)),
                ('tel', models.CharField(blank=True, max_length=16, null=True)),
                ('content', models.TextField(blank=True, max_length=256, null=True)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Setvalue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myid', models.IntegerField(default=0)),
                ('a_per', models.FloatField(default=20)),
                ('b_per', models.FloatField(default=20)),
                ('c_per', models.FloatField(default=20)),
                ('d_per', models.FloatField(default=20)),
                ('e_per', models.FloatField(default=20)),
            ],
        ),
    ]
