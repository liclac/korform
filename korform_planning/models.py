from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.sites.models import Site
from .util import format_datetime, format_datetime_diff

class Group(models.Model):
    class Meta:
        ordering = ['sort']
    
    site = models.ForeignKey(Site, related_name='groups')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20)
    sort = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    
    def get_absolute_url(self):
        return reverse('group', kwargs={'slug': self.slug})
    
    def __unicode__(self):
        return self.code

class Term(models.Model):
    site = models.ForeignKey(Site, related_name='terms')
    name = models.CharField(max_length=100)
    groups = models.ManyToManyField(Group, related_name='terms')
    form = models.ForeignKey('Form', related_name='term', null=True, blank=True)
    
    def __unicode__(self):
        return self.name

class Event(models.Model):
    class Meta:
        ordering = ['position']
    
    term = models.ForeignKey(Term, related_name='events')
    groups = models.ManyToManyField(Group, related_name='events')
    name = models.CharField(max_length=100)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    subtitle = models.CharField(max_length=100, blank=True)
    info = models.TextField(blank=True)
    no_answer = models.BooleanField(default=False)
    position = models.PositiveIntegerField(null=True)
    
    def get_subtitle(self):
        parts = []
        if self.start:
            if self.end:
                parts.append(format_datetime_diff(self.start, self.end))
            else:
                parts.append(format_datetime(self.start))
        if self.subtitle:
            parts.append(self.subtitle)
        return u", ".join(parts)
    
    def __unicode__(self):
        group_codes = self.groups.values_list('code', flat=True)
        return u"{0} ({1})".format(self.name, u', '.join(group_codes))

class Form(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name

class FormField(models.Model):
    class Meta:
        ordering = ['position']
    
    FIELD_CHOICES = (
        ('django.forms.CharField', u"Text field"),
        ('django.forms.BooleanField', u"Checkbox"),
    )
    
    form = models.ForeignKey(Form, related_name='fields')
    position = models.PositiveIntegerField(null=True)
    key = models.CharField(max_length=20)
    
    label = models.CharField(max_length=100)
    field = models.CharField(max_length=100, choices=FIELD_CHOICES)
    placeholder = models.CharField(max_length=100)
    help_text = models.TextField(blank=True)
    required = models.BooleanField(default=True)
    
    public = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.label
