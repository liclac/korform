# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_accounts', '0004_auto_20151105_2207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitekey',
            name='user',
        ),
        migrations.AddField(
            model_name='invitekey',
            name='profile',
            field=models.ForeignKey(related_name='invite_keys', default=1, to='korform_accounts.Profile'),
            preserve_default=False,
        ),
    ]
