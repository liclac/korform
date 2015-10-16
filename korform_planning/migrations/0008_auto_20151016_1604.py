# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_planning', '0007_auto_20151015_1828'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['sort']},
        ),
        migrations.AddField(
            model_name='group',
            name='sort',
            field=models.CharField(default=None, max_length=10),
            preserve_default=False,
        ),
    ]
