# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import korform_accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_accounts', '0002_auto_20151029_1937'),
    ]

    operations = [
        migrations.CreateModel(
            name='InviteKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(help_text='If this is blank, a new key will be generated.', max_length=20, blank=True)),
                ('expires', models.DateTimeField(default=korform_accounts.models.default_invite_key_expiry, help_text='Default is 30 days from now.')),
                ('user', models.ForeignKey(related_name='invite_keys', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
