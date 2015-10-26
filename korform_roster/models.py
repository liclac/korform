from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site
from jsonfield import JSONField
from korform_planning.models import Event

class Member(models.Model):
    profile = models.ForeignKey('korform_accounts.Profile', related_name='members')
    group = models.ForeignKey('korform_planning.Group', related_name='members')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()
    extra = JSONField(default={})
    
    def get_full_name(self):
        return u"{0} {1}".format(self.first_name, self.last_name)
    
    def get_events_missing_rsvp(self):
        return Event.objects.exclude(rsvps__member_id=self.id)
    
    def get_fields_missing_value(self, keys=[]):
        if not keys:
            keys = self.get_extra_keys()
        return [ key for key in keys if key not in self.extra ]
    
    def get_badge_count(self, request):
        count = 0
        url_name = request.resolver_match.url_name
        url_pk = request.resolver_match.kwargs.get('pk', 0)
        pk_match = unicode(self.pk) == url_pk
        
        if url_name != 'member_rsvp' or not pk_match:
            count += self.get_events_missing_rsvp().count()
        
        keys = self.get_extra_keys()
        if url_name != 'member_edit' or not pk_match:
            count += len(self.get_fields_missing_value(keys))
        
        return count
    
    def get_absolute_url(self):
        return reverse('member', kwargs={ 'pk': self.pk })
    
    def get_extra_keys(self):
        site = Site.objects.get_current()
        form = site.config.current_term.form
        if form:
            return [field.key for field in form.fields.all()]
        return []
    
    def __unicode__(self):
        return self.get_full_name()

class Contact(models.Model):
    profile = models.ForeignKey('korform_accounts.Profile', related_name='contacts')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    extra = JSONField(default={})
    
    def get_full_name(self):
        return u"{0} {1}".format(self.first_name, self.last_name)
    
    def get_absolute_url(self):
        return reverse('contact', kwargs={ 'pk': self.pk })
    
    def __unicode__(self):
        return self.get_full_name()

class RSVP(models.Model):
    CHOICES = (
        (1, _(u"Yes")),
        (0, _(u"No")),
        (2, _(u"Maybe")),
    )
    
    member = models.ForeignKey(Member, related_name='rsvps')
    event = models.ForeignKey('korform_planning.Event', related_name='rsvps')
    answer = models.IntegerField(choices=CHOICES)
    comment = models.TextField(blank=True)
