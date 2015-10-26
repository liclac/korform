# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('korform_roster', '0006_auto_20151026_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='extra',
            field=jsonfield.fields.JSONField(default={}, blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='extra',
            field=jsonfield.fields.JSONField(default={}, blank=True),
        ),
    ]
