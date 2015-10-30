import datetime
from django.test import TestCase
from django.contrib.sites.models import Site
from korform_accounts.models import Profile
from korform_planning.models import Group
from .models import Member, RSVP

class TestMember(TestCase):
    def setUp(self):
        self.site = Site.objects.create(domain=u"google.com", name=u"Google")
        self.group = Group.objects.create(site=self.site, name=u"Group", code=u"g", slug=u"g", sort=u"g")
        
        self.profile = Profile.objects.create()
        self.john_smith = Member.objects.create(
            site=self.site, profile=self.profile, group=self.group,
            first_name=u"John", last_name=u"Smith",
            birthday=datetime.datetime(2000,12,24),
        )
    
    def test_full_name(self):
        '''get_full_name() should work as expected.'''
        self.assertEqual(self.john_smith.get_full_name(), u"John Smith")
