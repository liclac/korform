# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_planning', '0016_auto_20151030_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sheetcolumn',
            name='format_string',
            field=models.TextField(help_text='A <a href="https://docs.python.org/2/library/string.html#string-formatting">format()</a> string. If <em>key</em> is given, its value is passed as {0}, additional keys as {1}, {2}, etc. All fields available in <em>key</em> are available.<br />If not given, all listed keys will be printed, separated by spaces.', blank=True),
        ),
    ]
