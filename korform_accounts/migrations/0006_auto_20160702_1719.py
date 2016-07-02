# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('korform_accounts', '0005_auto_20151106_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile',
            field=models.ForeignKey(related_name='users', on_delete=django.db.models.deletion.SET_NULL, to='korform_accounts.Profile', help_text='Multiple users may be associated with a single profile. These users will have access to the same data, but with different logins.', null=True),
        ),
    ]
