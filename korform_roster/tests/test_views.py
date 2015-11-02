import datetime
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from korform_accounts.models import User, Profile
from korform_planning.models import Term, Group
from korform_roster.models import Member

class MemberViewSetUpMixin(object):
    def setUp(self):
        self.site = Site.objects.first()
        
        self.group = Group.objects.create(site=self.site, name=u"Test Group", code='g', slug='g', sort='a')
        self.group2 = Group.objects.create(site=self.site, name=u"Group 2", code='g2', slug='g2', sort='b')
        self.group3 = Group.objects.create(site=self.site, name=u"Group 3", code='g3', slug='g3', sort='c')
        
        self.term = Term.objects.create(site=self.site, name=u"Test Term")
        self.term.groups = [self.group, self.group2]
        
        self.site.config.current_term = self.term
        self.site.config.save()
        
        self.profile = Profile.objects.create()
        self.member = Member.objects.create(
            site=self.site, group=self.group, profile=self.profile,
            first_name=u"First", last_name=u"Last", birthday=datetime.date(2000, 12, 24),
        )
        self.member2 = Member.objects.create(
            site=self.site, group=self.group3, profile=self.profile,
            first_name=u"Santa", last_name=u"Claus", birthday=datetime.date(1800, 12, 24),
        )
        
        self.user = User.objects.create_user(username='username', password='password')
        self.client = Client()
        self.client.login(username='username', password='password')

class TestMemberView(MemberViewSetUpMixin, TestCase):
    def test_unauthenticated(self):
        self.client.logout()
        path = reverse('member', kwargs={'pk': self.member.pk})
        res = self.client.get(path)
        self.assertRedirects(res, reverse('auth_login') + "?next=" + path)
    
    def test_access(self):
        res = self.client.get(reverse('member', kwargs={'pk': self.member.pk}))
        self.assertEqual(200, res.status_code)
        self.assertEqual(self.member.pk, res.context['member'].pk)
    
    def test_nonexistent(self):
        res = self.client.get(reverse('member', kwargs={'pk': 255}))
        self.assertEqual(404, res.status_code)

class TestMemberPickGroupView(MemberViewSetUpMixin, TestCase):
    def test_unauthenticated(self):
        self.client.logout()
        path = reverse('member_add')
        res = self.client.get(path)
        self.assertRedirects(res, reverse('auth_login') + "?next=" + path)
    
    def test_access(self):
        res = self.client.get(reverse('member_add'))
        self.assertEqual(200, res.status_code)
        self.assertEqual([self.group.pk, self.group2.pk], [g.pk for g in res.context['groups']])
    
    def test_no_term(self):
        self.site.config.current_term = None
        self.site.config.save()
        
        res = self.client.get(reverse('member_add'))
        self.assertEqual(200, res.status_code)
        self.assertEqual([], res.context['groups'])

class TestMemberCreateView(MemberViewSetUpMixin, TestCase):
    def test_unauthenticated(self):
        self.client.logout()
        path = reverse('member_add2', kwargs={'group': 'g'})
        res = self.client.get(path)
        self.assertRedirects(res, reverse('auth_login') + "?next=" + path)
    
    def test_access(self):
        res = self.client.get(reverse('member_add2', kwargs={'group': 'g'}))
        self.assertEqual(200, res.status_code)
        self.assertEqual(self.group.pk, res.context['group'].pk)
    
    def test_nonexistent(self):
        res = self.client.get(reverse('member_add2', kwargs={'group': 'gg'}))
        self.assertEqual(404, res.status_code)
    
    def test_inactive(self):
        res = self.client.get(reverse('member_add2', kwargs={'group': 'g3'}))
        self.assertEqual(404, res.status_code)
