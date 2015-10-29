# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_planning', '0011_auto_20151029_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sheetcolumn',
            name='format_string',
            field=models.TextField(default='{0}', help_text='A <a href="https://docs.python.org/2/library/string.html#string-formatting">format()</a> string. If <em>key</em> is given, its value is passed as {0}, additional keys as {1}, {2}, etc. All fields available in <em>key</em> are available.', blank=True),
        ),
        migrations.AlterField(
            model_name='sheetcolumn',
            name='key',
            field=models.CharField(help_text='You can list multiple keys, separated by ";". All custom keys are available, along with: <strong>first_name</strong>, <strong>last_name</strong>, <strong>birthday</strong>, <strong>group_name</strong>, <strong>group_code</strong>.', max_length=20, blank=True),
        ),
    ]
