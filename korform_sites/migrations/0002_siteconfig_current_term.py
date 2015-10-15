# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_planning', '0001_initial'),
        ('korform_sites', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfig',
            name='current_term',
            field=models.ForeignKey(related_name='current_for', blank=True, to='korform_planning.Term', null=True),
        ),
    ]
