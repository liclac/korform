# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('korform_roster', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='extra',
            field=jsonfield.fields.JSONField(default={}),
        ),
    ]
