from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils.functional import cached_property
from django.contrib.sites.models import Site
from jsonfield import JSONField
from korform_planning.models import Event

class ExtraDataMixin(object):
    @cached_property
    def extra_data(self):
        return self.get_extra_data()
    
    @cached_property
    def extra_keys(self):
        return self.get_extra_keys()
    
    @cached_property
    def fields_missing_value(self):
        return self.get_fields_missing_value()
    
    @cached_property
    def custom_form(self):
        return self.get_custom_form()
    
    @cached_property
    def custom_form_fields(self):
        return self.custom_form.fields.all() if self.custom_form else []
    
    def get_extra_data(self):
        data = []
        for field in self.custom_form_fields:
            data.append({
                'key': field.key,
                'label': field.label,
                'help_text': field.help_text,
                'public': field.public,
                'value': self.extra.get(field.key, None)
            })
        return data
    
    def get_extra_keys(self):
        return [field.key for field in self.custom_form_fields]
    
    def get_fields_missing_value(self):
        return [ key for key in self.extra_keys if key not in (self.extra or {}) ]

class Member(ExtraDataMixin, models.Model):
    '''
    A member of your organization.
    
    Members are associated with profiles and groups, and may have custom "Extra" data as specified
    by a [Form](/admin/korform_planning/form).  
    The form for members is set on a [term](/admin/korform_planning/term/), and may change at any
    time.
    '''
    
    site = models.ForeignKey(Site, related_name='members')
    profile = models.ForeignKey('korform_accounts.Profile', related_name='members')
    group = models.ForeignKey('korform_planning.Group', related_name='members')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()
    extra = JSONField(default={}, blank=True)
    
    @cached_property
    def events_missing_rsvp(self):
        return self.get_events_missing_rsvp()
    
    def get_full_name(self):
        return u"{0} {1}".format(self.first_name, self.last_name)
    
    def get_custom_form(self):
        term = self.site.config.current_term
        return term.form if term else None
    
    def get_events_missing_rsvp(self):
        return self.group.events.exclude(rsvps__member_id=self.id)
    
    def get_badge_count(self, request):
        count = 0
        url_name = request.resolver_match.url_name if request.resolver_match else None
        url_pk = request.resolver_match.kwargs.get('pk', 0) if request.resolver_match else None
        pk_match = unicode(self.pk) == url_pk
        
        if url_name != 'member_rsvp' or not pk_match:
            count += len(self.events_missing_rsvp)
        
        if url_name != 'member_edit' or not pk_match:
            count += len(self.fields_missing_value)
        
        return count
    
    def get_absolute_url(self):
        return reverse('member', kwargs={ 'pk': self.pk })
    
    def __unicode__(self):
        return self.get_full_name()

class Contact(ExtraDataMixin, models.Model):
    '''
    A contact for your organization members.
    
    These are assumed to be contactable if anything were to happen to any
    [member](/admin/korform_roster/member/) sharing their profile.  
    The form for contacts is also customizable, and is set on a [site](/admin/sites/site/).
    '''
    
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
    
    def css_class(self):
        return {1: 'success', 0: 'danger', 2: 'warning'}.get(self.answer, 'default')
