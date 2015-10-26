# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_roster', '0003_rsvp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rsvp',
            name='answer',
            field=models.IntegerField(choices=[(1, 'Yes'), (0, 'No'), (2, 'Maybe')]),
        ),
    ]
