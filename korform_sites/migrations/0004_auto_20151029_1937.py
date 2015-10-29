# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korform_sites', '0003_siteconfig_contact_form'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteconfig',
            name='contact_form',
            field=models.ForeignKey(related_name='contact_form_for', blank=True, to='korform_planning.Form', help_text='Determines any additional information requested of Contacts. Contacts are not tied to a term, but to the members sharing their profile.', null=True),
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='current_term',
            field=models.ForeignKey(related_name='current_for', blank=True, to='korform_planning.Term', help_text='The current term determines which events need RSVPs, what information is required of members, etc.', null=True),
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='term_contact',
            field=models.CharField(default='contact', help_text="Your site's term for a contact.", max_length=20, verbose_name='Term: Contact'),
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='term_contacts',
            field=models.CharField(default='contacts', help_text='Plural form of the above.', max_length=20, verbose_name='Term: Contacts'),
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='term_member',
            field=models.CharField(default='member', help_text="Your site's term for a member.", max_length=20, verbose_name='Term: Member'),
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='term_members',
            field=models.CharField(default='members', help_text='Plural form of the above.', max_length=20, verbose_name='Term: Members'),
        ),
    ]
