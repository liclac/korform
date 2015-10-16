import datetime
from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from grappelli.forms import GrappelliSortableHiddenMixin
from .models import Group, Term, Event, Form, FormField

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'site')
    list_filter = ('site__name',)
    search_fields = ('name', 'code')
    prepopulated_fields = { 'slug': ('code',), 'sort': ('code',) }



def event_date(field, display):
    def event_date_inner(event):
        v = getattr(event, field)
        if v is None:
            return u""
        elif v.hour == 0 and v.minute == 0:
            return v.date()
        return v
    event_date_inner.short_description = display
    return event_date_inner

def event_groups(event):
    return u", ".join(event.groups.values_list('code', flat=True))
event_groups.short_description = u"Groups"

class EventMonthListFilter(admin.SimpleListFilter):
    title = _(u"Month")
    parameter_name = 'month'
    
    def lookups(self, request, model_admin):
        return (
            (1, _(u"January")), (2, _(u"February")),
            (3, _(u"March")), (4, _(u"April")),
            (5, _(u"May")), (6, _(u"June")),
            (7, _(u"July")), (8, _(u"August")),
            (9, _(u"September")), (10, _(u"October")),
            (11, _(u"November")), (12, _(u"December")),
        )
    
    def queryset(self, request, queryset):
        month = self.value()
        if month:
            return queryset.filter(start__month=self.value())
        return queryset

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        event_date('start', u"Start"),
        event_date('end', u"End"),
        'subtitle',
        'no_answer',
        event_groups,
        'term'
    )
    
    list_filter = (
        'term__name',
        EventMonthListFilter,
        'no_answer',
        'groups',
    )
    
    search_fields = ('name', 'subtitle', 'info', 'groups__code')



def term_groups(term):
    return u", ".join(term.groups.values_list('code', flat=True))
term_groups.short_description = u"Groups"

class TermSiteFilter(admin.SimpleListFilter):
    title = _(u"Site")
    parameter_name = 'site'
    
    def lookups(self, request, model_admin):
        return [
            (s.id, s) for s in Site.objects.all()
        ]
    
    def queryset(self, request, queryset):
        month = self.value()
        if month:
            return queryset.filter(start__month=self.value())
        return queryset

class EventInline(GrappelliSortableHiddenMixin, admin.StackedInline):
    model = Event
    sortable_field_name = 'position'

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    inlines = [EventInline]
    list_display = ('name', term_groups, 'site')
    list_filter = (TermSiteFilter,)
    search_fields = ('name',)



class FormFieldInline(GrappelliSortableHiddenMixin, admin.StackedInline):
    model = FormField
    sortable_field_name = 'position'

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    inlines = [FormFieldInline]
