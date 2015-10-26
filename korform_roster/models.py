from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site
from jsonfield import JSONField
from korform_planning.models import Event

class ExtraDataMixin(object):
    def get_extra_data(self):
        form = self.get_custom_form()
        data = []
        if form:
            for field in form.fields.all():
                data.append({
                    'key': field.key,
                    'label': field.label,
                    'help_text': field.help_text,
                    'public': field.public,
                    'value': self.extra.get(field.key, None)
                })
        return data
    
    def get_extra_keys(self):
        form = self.get_custom_form()
        if form:
            return [field.key for field in form.fields.all()]
        return []
    
    def get_fields_missing_value(self, keys=[]):
        if not keys:
            keys = self.get_extra_keys()
        return [ key for key in keys if key not in (self.extra or {}) ]

class Member(ExtraDataMixin, models.Model):
    site = models.ForeignKey(Site, related_name='members')
    profile = models.ForeignKey('korform_accounts.Profile', related_name='members')
    group = models.ForeignKey('korform_planning.Group', related_name='members')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()
    extra = JSONField(default={}, blank=True)
    
    def get_full_name(self):
        return u"{0} {1}".format(self.first_name, self.last_name)
    
    def get_custom_form(self):
        term = self.site.config.current_term
        return term.form if term else None
    
    def get_events_missing_rsvp(self):
        return Event.objects.exclude(rsvps__member_id=self.id)
    
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
    
    def __unicode__(self):
        return self.get_full_name()

class Contact(ExtraDataMixin, models.Model):
    site = models.ForeignKey(Site, related_name='contacts')
    profile = models.ForeignKey('korform_accounts.Profile', related_name='contacts')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    extra = JSONField(default={}, blank=True)
    
    def get_full_name(self):
        return u"{0} {1}".format(self.first_name, self.last_name)
    
    def get_custom_form(self):
        return self.site.config.contact_form
    
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
