# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_accounts', '0001_initial'),
        ('korform_planning', '0002_groups'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('birthday', models.DateField()),
                ('group', models.ForeignKey(related_name='members', to='korform_planning.Group')),
                ('profile', models.ForeignKey(related_name='members', to='korform_accounts.Profile')),
            ],
        ),
    ]
