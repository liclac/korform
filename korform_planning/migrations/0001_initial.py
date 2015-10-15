# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('start', models.DateTimeField(null=True, blank=True)),
                ('end', models.DateTimeField(null=True, blank=True)),
                ('subtitle', models.CharField(max_length=100, blank=True)),
                ('info', models.TextField(blank=True)),
                ('no_answer', models.BooleanField(default=False)),
                ('position', models.PositiveIntegerField(null=True)),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('site', models.ForeignKey(related_name='terms', to='sites.Site')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='term',
            field=models.ForeignKey(related_name='events', to='korform_planning.Term'),
        ),
    ]
