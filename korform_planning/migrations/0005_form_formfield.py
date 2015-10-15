# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_planning', '0004_group_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('message', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveIntegerField(null=True)),
                ('key', models.CharField(max_length=20)),
                ('label', models.CharField(max_length=100)),
                ('field', models.CharField(max_length=100, choices=[(b'django.forms.CharField', 'Text field'), (b'django.forms.TextField', 'Textarea'), (b'django.forms.BooleanField', 'Checkbox')])),
                ('placeholder', models.CharField(max_length=100)),
                ('help_text', models.TextField(blank=True)),
                ('required', models.BooleanField(default=True)),
                ('public', models.BooleanField(default=True)),
                ('form', models.ForeignKey(related_name='fields', to='korform_planning.Form')),
            ],
        ),
    ]
