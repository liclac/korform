# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_planning', '0010_auto_20151026_1655'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sheet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SheetColumn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveIntegerField(null=True)),
                ('label', models.CharField(max_length=100, blank=True)),
                ('key', models.CharField(max_length=20, blank=True)),
                ('format_string', models.TextField(default='{0}', blank=True)),
                ('default', models.CharField(help_text='Displayed instead of an empty cell.', max_length=100, blank=True)),
                ('sheet', models.ForeignKey(related_name='columns', to='korform_planning.Sheet')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.AddField(
            model_name='term',
            name='sheet',
            field=models.ForeignKey(related_name='sheet', blank=True, to='korform_planning.Sheet', null=True),
        ),
    ]
