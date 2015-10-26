# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('korform_roster', '0005_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='site',
            field=models.ForeignKey(related_name='contacts', default=1, to='sites.Site'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='site',
            field=models.ForeignKey(related_name='members', default=1, to='sites.Site'),
            preserve_default=False,
        ),
    ]
