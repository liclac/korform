# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_planning', '0008_auto_20151016_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formfield',
            name='placeholder',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
