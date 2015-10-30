# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_planning', '0017_auto_20151030_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sheetcolumn',
            name='label',
            field=models.CharField(max_length=100),
        ),
    ]
