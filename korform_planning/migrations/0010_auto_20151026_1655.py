# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_planning', '0009_auto_20151026_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formfield',
            name='field',
            field=models.CharField(max_length=100, choices=[(b'textfield', 'Text field'), (b'textarea', 'Textarea'), (b'checkbox', 'Checkbox')]),
        ),
    ]
