import datetime
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from korform_accounts.models import Profile, User
from korform_planning.models import Group, Term, Form, FormField, Sheet, SheetColumn
from korform_roster.models import Member
from korform_planning.views import GroupView

class TestGroupView(TestCase):
    def setUp(self):
        self.site = Site.objects.get(pk=1)
        
        self.profile = Profile.objects.create()
        
        self.group = Group.objects.create(site=self.site, name=u"Group", code=u'g', slug=u'g', sort=u'g')
        self.member = Member.objects.create(
            group=self.group, site=self.site, profile=self.profile,
            first_name=u"John", last_name=u"Smith", birthday=datetime.date(2000, 12, 24),
            extra={ 'key1': u"Smith 1", 'key2': u"Smith 2" }
        )
        self.member2 = Member.objects.create(
            group=self.group, site=self.site, profile=self.profile,
            first_name=u"John", last_name=u"Doe", birthday=datetime.date(2001, 10, 11),
            extra={ 'key1': u"Doe 1", 'key2': u"Doe 2" }
        )
        
        self.term = Term.objects.create(site=self.site, name=u"Test Term")
        self.term.groups=[self.group]
        
        self.form = Form.objects.create(name=u"Test Form")
        self.form.fields = [
            FormField(position=0, key='key1', field='textfield', label=u"Field 1"),
            FormField(position=1, key='key2', field='textfield', label=u"Field 2"),
        ]
        self.form.save()
        
        self.sheet = Sheet.objects.create(name=u"Test Sheet")
        self.sheet.columns = [
            SheetColumn(position=0, key='first_name', label=u"First name"),
            SheetColumn(position=1, key='last_name', label=u"Last name"),
        ]
        self.sheet.save()
        
        self.site.config.current_term = self.term
        self.site.config.save()
        
        self.user = User.objects.create_user(username='username', password='password')
        self.client = Client()
        self.client.login(username='username', password='password')
    
    def test_unauthenticated(self):
        self.client.logout()
        path = reverse('group', kwargs={'slug': 'g'})
        res = self.client.get(path)
        self.assertRedirects(res, reverse('auth_login') + "?next=" + path)
    
    def test_access(self):
        res = self.client.get(reverse('group', kwargs={'slug': 'g'}))
        self.assertEqual(200, res.status_code)
        self.assertEqual(self.group.pk, res.context['group'].pk)
        self.assertEqual([self.member2.pk, self.member.pk], [m.pk for m in res.context['members']])
    
    def test_nonexistent(self):
        res = self.client.get(reverse('group', kwargs={'slug': 'aaaa'}))
        self.assertEqual(404, res.status_code)
    
    def test_inactive(self):
        self.term.groups = []
        self.term.save()
        
        res = self.client.get(reverse('group', kwargs={'slug': 'g'}))
        self.assertEqual(404, res.status_code)
    
    def test_no_term(self):
        self.site.config.current_term = None
        self.site.config.save()
        
        res = self.client.get(reverse('group', kwargs={'slug': 'g'}))
        self.assertEqual(404, res.status_code)
    
    def test_term_no_form_or_sheet(self):
        res = self.client.get(reverse('group', kwargs={'slug': 'g'}))
        self.assertEqual(200, res.status_code)
        
        self.assertEqual(2, len(res.context['columns']))
        self.assertEqual(u"Name", res.context['columns'][0].label)
        self.assertEqual(u"Birthday", res.context['columns'][1].label)
    
    def test_term_form_only(self):
        self.term.form = self.form
        self.term.save()
        
        res = self.client.get(reverse('group', kwargs={'slug': 'g'}))
        self.assertEqual(200, res.status_code)
        
        self.assertEqual(u"Name", res.context['columns'][0].label)
        self.assertEqual(u"Birthday", res.context['columns'][1].label)
        self.assertEqual(u"Field 1", res.context['columns'][2].label)
        self.assertEqual(u"Field 2", res.context['columns'][3].label)
        
        self.assertEqual(u"John Doe", res.context['rows'][0]['columns'][0]['value'])
        self.assertEqual(u"2001-10-11", res.context['rows'][0]['columns'][1]['value'])
        self.assertEqual(u"Doe 1", res.context['rows'][0]['columns'][2]['value'])
        self.assertEqual(u"Doe 2", res.context['rows'][0]['columns'][3]['value'])
    
    def test_term_with_sheet(self):
        self.term.sheet = self.sheet
        self.term.save()
        
        res = self.client.get(reverse('group', kwargs={'slug': 'g'}))
        self.assertEqual(200, res.status_code)
        
        self.assertEqual(u"First name", res.context['columns'][0].label)
        self.assertEqual(u"Last name", res.context['columns'][1].label)
        
        self.assertEqual(u"John", res.context['rows'][0]['columns'][0]['value'])
        self.assertEqual(u"Doe", res.context['rows'][0]['columns'][1]['value'])
