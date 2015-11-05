# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_accounts', '0003_invitekey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitekey',
            name='key',
            field=models.CharField(help_text='If this is blank, a new key will be generated.', unique=True, max_length=20, blank=True),
        ),
    ]
