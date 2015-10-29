# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_planning', '0012_auto_20151029_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(help_text='To specify only the date, leave the time to 00:00.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='info',
            field=models.TextField(help_text='Displayed under the subtitle. Allows Markdown.', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='no_answer',
            field=models.BooleanField(default=False, help_text="This event should merely be noted on members' calendars, but no RSVP is requested. [NOT YET FUNCTIONAL]"),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(help_text='To specify only the date, leave the time to 00:00.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='subtitle',
            field=models.CharField(help_text='Displayed along with the duration. Can be used to describe durations not expressable with a simple start/end.', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='form',
            name='message',
            field=models.TextField(help_text='Displayed at the top of the form. Allows Markdown.', blank=True),
        ),
        migrations.AlterField(
            model_name='form',
            name='name',
            field=models.CharField(help_text='Not shown to users.', max_length=100),
        ),
        migrations.AlterField(
            model_name='formfield',
            name='key',
            field=models.CharField(help_text='Unique key used to store the data. Choose carefully; if you change it, old data will be disassociated from the field, but still remain with the old key!', max_length=20),
        ),
        migrations.AlterField(
            model_name='formfield',
            name='public',
            field=models.BooleanField(default=True, help_text='Public fields are displayed on public detail pages, and included in sheets by default.'),
        ),
        migrations.AlterField(
            model_name='formfield',
            name='required',
            field=models.BooleanField(default=True, help_text='For checkbox fields, this requires it to be checked.'),
        ),
        migrations.AlterField(
            model_name='group',
            name='code',
            field=models.CharField(help_text='A shorthand "code name" for the group.', max_length=20),
        ),
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.TextField(help_text="If given, will be displayed on the group's page. Allows Markdown.", blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(help_text='The full name of the group.', max_length=100),
        ),
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(help_text='Normalized identifier used in URLs.', max_length=20),
        ),
        migrations.AlterField(
            model_name='group',
            name='sort',
            field=models.CharField(help_text='Groups are sorted (alphabetically) by this in menus. Not shown to users.', max_length=10),
        ),
        migrations.AlterField(
            model_name='sheet',
            name='name',
            field=models.CharField(help_text='Not visible to users.', max_length=100),
        ),
        migrations.AlterField(
            model_name='term',
            name='form',
            field=models.ForeignKey(related_name='term', blank=True, to='korform_planning.Form', help_text='A Form allows you to add custom input fields to members. Three fields are hardcoded: <em>first name</em>, <em>last name</em> and <em>birthday</em>.<br />If none is given, only these three are displayed.', null=True),
        ),
        migrations.AlterField(
            model_name='term',
            name='name',
            field=models.CharField(help_text='Not visible to users.', max_length=100),
        ),
        migrations.AlterField(
            model_name='term',
            name='sheet',
            field=models.ForeignKey(related_name='sheet', blank=True, to='korform_planning.Sheet', help_text='A Sheet allows you to customize the presentation of group sheets.<br />If none is given, sheet presentation is inferred from the Form.', null=True),
        ),
        migrations.AlterField(
            model_name='term',
            name='site',
            field=models.ForeignKey(related_name='terms', to='sites.Site', help_text='Remember to also mark a term as the "current" one, in the site\'s configuration.'),
        ),
    ]
