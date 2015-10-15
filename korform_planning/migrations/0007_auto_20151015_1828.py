# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_planning', '0006_term_form'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='formfield',
            options={'ordering': ['position']},
        ),
        migrations.AlterField(
            model_name='formfield',
            name='field',
            field=models.CharField(max_length=100, choices=[(b'django.forms.CharField', 'Text field'), (b'django.forms.BooleanField', 'Checkbox')]),
        ),
    ]
