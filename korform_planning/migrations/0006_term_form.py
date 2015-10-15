# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_planning', '0005_form_formfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='form',
            field=models.ForeignKey(related_name='term', blank=True, to='korform_planning.Form', null=True),
        ),
    ]
