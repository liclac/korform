import datetime
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from korform_accounts.models import Profile
from korform_planning.models import Group, Term, Form, FormField, Sheet, SheetColumn
from korform_roster.models import Member
from korform_planning.views import GroupView

class TestGroupView(TestCase):
    def setUp(self):
        self.site = Site.objects.create(domain='google.com', name=u"Google")
        
        self.profile = Profile.objects.create()
        
        self.group = Group.objects.create(site=self.site, name=u"Group", code=u'g', slug=u'g', sort=u'g')
        self.member = Member.objects.create(group=self.group, site=self.site, profile=self.profile,
            first_name=u"John", last_name=u"Smith", birthday=datetime.date(2000, 12, 24))
        self.member2 = Member.objects.create(group=self.group, site=self.site, profile=self.profile,
            first_name=u"John", last_name=u"Doe", birthday=datetime.date(2001, 10, 11))
        
        self.term = Term.objects.create(site=self.site, name=u"Test Term")
        self.term.groups=[self.group]
        
        self.form = Form.objects.create(name=u"Test Form")
        self.form.fields = [
            FormField(key='first_name', field='textfield', label=u"Field 1"),
            FormField(key='last_name', field='textfield', label=u"Field 2"),
        ]
        
        self.sheet = Form.objects.create(name=u"Test Sheet")
        self.sheet.columns = [
            SheetColumn(key='first_name', label=u"Column 1"),
            SheetColumn(key='last_name', label=u"Column 2"),
        ]
        
        self.client = Client()
    
    def test_members(self):
        res = self.client.get(reverse('group', kwargs={'slug': 'g'}))
        self.assertEqual(200, res.status_code)
        self.assertEqual([self.member2.pk, self.member.pk], [m.pk for m in res.context['members']])
