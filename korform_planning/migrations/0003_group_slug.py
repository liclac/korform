# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string
from django.db import migrations, models

def random_slug():
    return ''.join([random.choice(string.ascii_lowercase) for _ in range(5)])

class Migration(migrations.Migration):

    dependencies = [
        ('korform_planning', '0002_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='slug',
            field=models.SlugField(default=random_slug, max_length=20),
            preserve_default=False,
        ),
    ]
