# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_planning', '0010_auto_20151026_1655'),
        ('korform_sites', '0002_siteconfig_current_term'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfig',
            name='contact_form',
            field=models.ForeignKey(related_name='contact_form_for', blank=True, to='korform_planning.Form', null=True),
        ),
    ]
