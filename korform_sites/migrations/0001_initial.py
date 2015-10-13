# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import annoying.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term_member', models.CharField(default='member', max_length=20)),
                ('term_members', models.CharField(default='members', max_length=20)),
                ('term_contact', models.CharField(default='contact', max_length=20)),
                ('term_contacts', models.CharField(default='contacts', max_length=20)),
                ('site', annoying.fields.AutoOneToOneField(related_name='config', to='sites.Site')),
            ],
        ),
    ]
