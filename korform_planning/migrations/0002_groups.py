# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('korform_planning', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=20)),
                ('site', models.ForeignKey(related_name='groups', to='sites.Site')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='groups',
            field=models.ManyToManyField(related_name='events', to='korform_planning.Group'),
        ),
        migrations.AddField(
            model_name='term',
            name='groups',
            field=models.ManyToManyField(related_name='terms', to='korform_planning.Group'),
        ),
    ]
