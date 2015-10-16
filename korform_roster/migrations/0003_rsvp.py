# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_planning', '0008_auto_20151016_1604'),
        ('korform_roster', '0002_member_extra'),
    ]

    operations = [
        migrations.CreateModel(
            name='RSVP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.IntegerField(choices=[(0, 'No'), (1, 'Yes'), (2, 'Maybe')])),
                ('comment', models.TextField(blank=True)),
                ('event', models.ForeignKey(related_name='rsvps', to='korform_planning.Event')),
                ('member', models.ForeignKey(related_name='rsvps', to='korform_roster.Member')),
            ],
        ),
    ]
