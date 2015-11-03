import datetime
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from korform_accounts.models import User, Profile
from korform_planning.models import Term, Group, Event, Form, FormField
from korform_roster.models import Member, RSVP

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
        
        self.form = Form.objects.create(name=u"Test Form")
        self.form.fields = [
            FormField(position=0, key='required', label=u"Required", field='textfield', required=True),
            FormField(position=1, key='optional', label=u"Optional", field='textfield', required=False),
        ]
        
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
    
    def test_create(self):
        res = self.client.post(reverse('member_add2', kwargs={'group': 'g'}), {
            'first_name': u"First",
            'last_name': u"Last",
            'birthday': u"2001-10-11",
        }, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'korform_roster/member_rsvp.html')
        self.assertEqual(res.context['member'].first_name, u"First")
        self.assertEqual(res.context['member'].last_name, u"Last")
        self.assertEqual(res.context['member'].birthday, datetime.date(2001, 10, 11))
        self.assertEqual(res.context['member'].extra, {})
    
    def test_create_custom_fields(self):
        self.term.form = self.form
        self.term.save()
        
        res = self.client.post(reverse('member_add2', kwargs={'group': 'g'}), {
            'first_name': u"First",
            'last_name': u"Last",
            'birthday': u"2001-10-11",
            'required': u"Required",
            'optional': u"Optional",
        }, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'korform_roster/member_rsvp.html')
        self.assertEqual(res.context['member'].extra, {
            u'required': u"Required",
            u'optional': u"Optional",
        })
    
    def test_create_custom_fields_no_optional(self):
        self.term.form = self.form
        self.term.save()
        
        res = self.client.post(reverse('member_add2', kwargs={'group': 'g'}), {
            'first_name': u"First",
            'last_name': u"Last",
            'birthday': u"2001-10-11",
            'required': u"Required",
        }, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'korform_roster/member_rsvp.html')
        self.assertEqual(res.context['member'].extra, {
            u'required': u"Required",
            u'optional': u"",
        })
    
    def test_create_missing_data(self):
        res = self.client.post(reverse('member_add2', kwargs={'group': 'g'}), {})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['form'].errors.keys(), ['first_name', 'last_name', 'birthday'])
    
    def test_create_missing_data_custom_fields(self):
        self.term.form = self.form
        self.term.save()
        
        res = self.client.post(reverse('member_add2', kwargs={'group': 'g'}), {
            'first_name': u"First",
            'last_name': u"Last",
            'birthday': u"2001-10-11",
        })
        self.assertEqual(res.context['form'].errors.keys(), ['required'])

class TestMemberRSVPView(MemberViewSetUpMixin, TestCase):
    def setUp(self):
        super(TestMemberRSVPView, self).setUp()
        
        self.event1 = Event.objects.create(term=self.term, name=u"Event 1")
        self.event1.groups = [self.group]
        
        self.event2 = Event.objects.create(term=self.term, name=u"Event 2")
        self.event2.groups = [self.group]
        
        self.event3 = Event.objects.create(term=self.term, name=u"Event 3")
        self.event3.groups = [self.group]
        
        self.event4 = Event.objects.create(term=self.term, name=u"Groupless Event")
    
    def test_unauthenticated(self):
        self.client.logout()
        path = reverse('member_rsvp', kwargs={'pk': self.member.pk})
        res = self.client.get(path)
        self.assertRedirects(res, reverse('auth_login') + "?next=" + path)
    
    def test_access(self):
        res = self.client.get(reverse('member_rsvp', kwargs={'pk': self.member.pk}))
        self.assertEqual(200, res.status_code)
        self.assertEqual(self.member.pk, res.context['member'].pk)
    
    def test_events(self):
        res = self.client.get(reverse('member_rsvp', kwargs={'pk': self.member.pk}))
        self.assertEqual([e.pk for e in res.context['events']], [self.event1.pk, self.event2.pk, self.event3.pk])
    
    def test_submit(self):
        res = self.client.post(reverse('member_rsvp', kwargs={'pk': self.member.pk}), {
            'form-TOTAL_FORMS': 3, 'form-INITIAL_FORMS': 0,
            'form-MIN_NUM_FORMS': 2, 'form-MAX_NUM_FORMS': 2,
            'form-0-answer': 1, 'form-0-comment': u"",
            'form-1-answer': 2, 'form-1-comment': u"Comment",
            'form-2-answer': 0, 'form-2-comment': u"",
        }, follow=True)
        self.assertTemplateUsed(res, 'korform_roster/member_detail.html')
        self.assertEqual(len(self.member.get_events_missing_rsvp()), 0)
        
        rsvp1 = RSVP.objects.get(member=self.member, event=self.event1)
        self.assertEqual(rsvp1.answer, 1)
        self.assertEqual(rsvp1.comment, u"")
        
        rsvp2 = RSVP.objects.get(member=self.member, event=self.event2)
        self.assertEqual(rsvp2.answer, 2)
        self.assertEqual(rsvp2.comment, u"Comment")
        
        rsvp3 = RSVP.objects.get(member=self.member, event=self.event3)
        self.assertEqual(rsvp3.answer, 0)
        self.assertEqual(rsvp3.comment, u"")
    
    def test_submit_missing_form(self):
        res = self.client.post(reverse('member_rsvp', kwargs={'pk': self.member.pk}), {
            'form-TOTAL_FORMS': 2, 'form-INITIAL_FORMS': 0,
            'form-MIN_NUM_FORMS': 2, 'form-MAX_NUM_FORMS': 2,
            'form-0-answer': 1, 'form-0-comment': u"",
            'form-1-answer': 2, 'form-1-comment': u"Comment",
        }, follow=True)
        self.assertTemplateUsed(res, 'korform_roster/member_detail.html')
        self.assertItemsEqual(self.member.get_events_missing_rsvp().values_list('pk', flat=True), [self.event3.pk])
    
    def test_submit_missing_field(self):
        res = self.client.post(reverse('member_rsvp', kwargs={'pk': self.member.pk}), {
            'form-TOTAL_FORMS': 3, 'form-INITIAL_FORMS': 0,
            'form-MIN_NUM_FORMS': 2, 'form-MAX_NUM_FORMS': 2,
            'form-0-answer': 1, 'form-0-comment': u"",
            'form-1-answer': 2, 'form-1-comment': u"Comment",
        })
        self.assertTemplateUsed(res, 'korform_roster/member_rsvp.html')
        self.assertItemsEqual(res.context['formset'].errors[2].keys(), ['answer'])
