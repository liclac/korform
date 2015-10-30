# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_planning', '0014_auto_20151030_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sheetcolumn',
            name='key',
            field=models.CharField(help_text='You can list multiple keys, separated by ",". All custom keys are available, along with: <strong>first_name</strong>, <strong>last_name</strong>, <strong>birthday</strong>, <strong>group_name</strong>, <strong>group_code</strong>.', max_length=255, blank=True),
        ),
    ]
