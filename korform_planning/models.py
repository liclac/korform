from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils.module_loading import import_string
from django.db import models
from django.contrib.sites.models import Site
from .util import format_datetime, format_datetime_diff

class Group(models.Model):
    class Meta:
        ordering = ['sort']
    
    site = models.ForeignKey(Site, related_name='groups')
    name = models.CharField(max_length=100, help_text=u"The full name of the group.")
    code = models.CharField(max_length=20, help_text=u"A shorthand \"code name\" for the group.")
    slug = models.SlugField(max_length=20, help_text=u"Normalized identifier used in URLs.")
    sort = models.CharField(max_length=10, help_text=u"Groups are sorted (alphabetically) by this in menus. Not shown to users.")
    description = models.TextField(blank=True, help_text=u"If given, will be displayed on the group's page. Allows Markdown.")
    
    def get_absolute_url(self):
        return reverse('group', kwargs={'slug': self.slug})
    
    def __unicode__(self):
        return self.code

class Term(models.Model):
    site = models.ForeignKey(Site, related_name='terms', help_text=u"Remember to also mark a term as the \"current\" one, in the site's configuration.")
    name = models.CharField(max_length=100, help_text=u"Not visible to users.")
    groups = models.ManyToManyField(Group, related_name='terms')
    form = models.ForeignKey('Form', related_name='term', null=True, blank=True, help_text=u"A Form allows you to add custom input fields to members. Three fields are hardcoded: <em>first name</em>, <em>last name</em> and <em>birthday</em>.<br />If none is given, only these three are displayed.")
    sheet = models.ForeignKey('Sheet', related_name='sheet', null=True, blank=True, help_text=u"A Sheet allows you to customize the presentation of group sheets.<br />If none is given, sheet presentation is inferred from the Form.")
    
    def __unicode__(self):
        return self.name

class Event(models.Model):
    class Meta:
        ordering = ['position']
    
    term = models.ForeignKey(Term, related_name='events')
    groups = models.ManyToManyField(Group, related_name='events')
    name = models.CharField(max_length=100)
    start = models.DateTimeField(null=True, blank=True, help_text=u"To specify only the date, leave the time to 00:00.")
    end = models.DateTimeField(null=True, blank=True, help_text=u"To specify only the date, leave the time to 00:00.")
    subtitle = models.CharField(max_length=100, blank=True, help_text=u"Displayed along with the duration. Can be used to describe durations not expressable with a simple start/end.")
    info = models.TextField(blank=True, help_text=u"Displayed under the subtitle. Allows Markdown.")
    no_answer = models.BooleanField(default=False, help_text=u"This event should merely be noted on members' calendars, but no RSVP is requested. [NOT YET FUNCTIONAL]")
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
    name = models.CharField(max_length=100, help_text=u"Not shown to users.")
    message = models.TextField(blank=True, help_text=u"Displayed at the top of the form. Allows Markdown.")
    
    def __unicode__(self):
        return self.name

class FormField(models.Model):
    class Meta:
        ordering = ['position']
    
    FIELD_CHOICES = (
        ('textfield', u"Text field"),
        ('textarea', u"Textarea"),
        ('checkbox', u"Checkbox"),
    )
    
    FIELDS = {
        'textfield': ('django.forms.CharField', 'django.forms.widgets.TextInput', {}),
        'textarea': ('django.forms.CharField', 'django.forms.widgets.Textarea', {'rows': 3}),
        'checkbox': ('django.forms.BooleanField', 'django.forms.widgets.CheckboxInput', {}),
    }
    
    form = models.ForeignKey(Form, related_name='fields')
    position = models.PositiveIntegerField(null=True)
    key = models.CharField(max_length=20, help_text=u"Unique key used to store the data. Choose carefully; if you change it, old data will be disassociated from the field, but still remain with the old key!")
    
    label = models.CharField(max_length=100)
    field = models.CharField(max_length=100, choices=FIELD_CHOICES)
    placeholder = models.CharField(max_length=100, blank=True)
    help_text = models.TextField(blank=True)
    required = models.BooleanField(default=True, help_text=u"For checkbox fields, this requires it to be checked.")
    
    public = models.BooleanField(default=True, help_text=u"Public fields are displayed on public detail pages, and included in sheets by default.")
    
    def create_field(self):
        f_cls_name, w_cls_name, attrs = FormField.FIELDS[self.field]
        f_cls = import_string(f_cls_name)
        w_cls = import_string(w_cls_name)
        f_kwargs = {
            'label': self.label,
            'help_text': self.help_text,
            'required': self.required,
        }
        attrs.update({
            'placeholder': self.placeholder,
        })
        return f_cls(widget=w_cls(attrs=attrs), **f_kwargs)
    
    def __unicode__(self):
        return self.label

class Sheet(models.Model):
    name = models.CharField(max_length=100, help_text=u"Not visible to users.")
    
    @classmethod
    def get_default_columns(cls):
        return [
            SheetColumn(position=0, label=_(u"Name"), key=u"first_name;last_name", format_string=u"{0} {1}"),
            SheetColumn(position=1, label=_(u"Birthday"), key=u"birthday"),
        ]
    
    @classmethod
    def columns_from_form(cls, form):
        defaults = cls.get_default_columns()
        return defaults + [
            SheetColumn(position=len(defaults) + i, label=field.label, key=field.key)
            for i, field in enumerate(form.fields.filter(public=True))
        ]
    
    def __unicode__(self):
        return self.name

class SheetColumn(models.Model):
    class Meta:
        ordering = ['position']
    
    sheet = models.ForeignKey(Sheet, related_name='columns')
    position = models.PositiveIntegerField(null=True)
    
    label = models.CharField(max_length=100, blank=True)
    key = models.CharField(max_length=20, blank=True, help_text=u"You can list multiple keys, separated by \",\". All custom keys are available, along with: <strong>first_name</strong>, <strong>last_name</strong>, <strong>birthday</strong>, <strong>group_name</strong>, <strong>group_code</strong>.")
    format_string = models.TextField(blank=True, default=u"{0}", help_text=u"A <a href=\"https://docs.python.org/2/library/string.html#string-formatting\">format()</a> string. If <em>key</em> is given, its value is passed as {0}, additional keys as {1}, {2}, etc. All fields available in <em>key</em> are available.")
    default = models.CharField(max_length=100, blank=True, help_text=u"Displayed instead of an empty cell.")
    
    def render(self, member):
        kwargs = {
            'first_name': member.first_name,
            'last_name': member.last_name,
            'birthday': member.birthday,
            'group_name': member.group.name,
            'group_code': member.group.code,
        }
        kwargs.update(member.extra)
        args = [ kwargs.get(key.strip(), '') for key in self.key.split(',') ]
        return self.format_string.format(*args, **kwargs).strip() or self.default
    
    def __unicode__(self):
        return self.label or self.key or "Field #{0}".format(self.position)



def clear_site_cache(instance, created, raw, **kwargs):
    Site.objects.clear_cache()

models.signals.post_save.connect(clear_site_cache, sender=Term, dispatch_uid='term_clear_cache')
models.signals.post_save.connect(clear_site_cache, sender=Group, dispatch_uid='group_clear_cache')
