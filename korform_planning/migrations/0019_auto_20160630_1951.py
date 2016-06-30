# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_planning', '0018_auto_20151030_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='no_answer',
            field=models.BooleanField(default=False, help_text="This event should merely be noted on members' calendars, but no RSVP is requested."),
        ),
    ]
