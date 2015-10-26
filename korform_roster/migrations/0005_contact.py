# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('korform_accounts', '0001_initial'),
        ('korform_roster', '0004_auto_20151026_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('extra', jsonfield.fields.JSONField(default={})),
                ('profile', models.ForeignKey(related_name='contacts', to='korform_accounts.Profile')),
            ],
        ),
    ]
