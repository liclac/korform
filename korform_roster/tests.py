import datetime
from django.test import TestCase
from django.contrib.sites.models import Site
from korform_accounts.models import Profile
from korform_planning.models import Group, Event, Term, Form, FormField
from .models import Member, RSVP

class TestMember(TestCase):
    def setUp(self):
        self.site = Site.objects.create(domain=u"google.com", name=u"Google")
        self.group = Group.objects.create(site=self.site, name=u"Group", code=u"g", slug=u"g", sort=u"g")
        
        self.form = Form.objects.create(name=u"Test Form")
        self.form.fields = [
            FormField(position=0, key='key', label=u"Label", field='textfield', help_text=u"Help text"),
        ]
        
        self.term = Term.objects.create(site=self.site, name=u"Test Term", form=self.form)
        self.term.groups = [self.group]
        
        self.event1 = Event.objects.create(position=0, term=self.term, name=u"Test Event")
        self.event1.groups = [self.group]
        self.event2 = Event.objects.create(position=1, term=self.term, name=u"Groupless Event")
        self.event2.groups = []
        
        self.site.config.current_term = self.term
        self.site.config.save()
        
        self.profile = Profile.objects.create()
        self.member = Member.objects.create(
            site=self.site, profile=self.profile, group=self.group,
            first_name=u"John", last_name=u"Smith",
            birthday=datetime.datetime(2000,12,24),
            extra={ 'key': u"Value", 'key2': u"Value 2" }
        )
    
    def test_full_name(self):
        self.assertEqual(self.member.get_full_name(), u"John Smith")
    
    def test_custom_form(self):
        self.assertEqual(self.form, self.member.get_custom_form())
    
    def test_extra_data(self):
        self.assertEqual(self.member.get_extra_data(), [
            {
                'key': u'key',
                'label': u"Label",
                'help_text': u"Help text",
                'public': True,
                'value': u"Value",
            }
        ])
    
    def test_extra_keys(self):
        self.assertEqual(self.member.get_extra_keys(), ['key'])
    
    def test_fields_missing_value_none(self):
        self.assertEqual(self.member.get_fields_missing_value(), [])
    
    def test_fields_missing_value_one(self):
        self.member.extra = {}
        self.assertEqual(self.member.get_fields_missing_value(), ['key'])
    
    def test_events_missing_rsvp_no_rsvps(self):
        self.assertEqual(self.member.get_events_missing_rsvp().count(), 1)
    
    def test_events_missing_rsvp_one_rsvp(self):
        self.member.rsvps = [
            RSVP(event=self.event1, answer=1),
        ]
        self.assertEqual(self.member.get_events_missing_rsvp().count(), 0)
