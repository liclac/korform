import datetime
from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from grappelli.forms import GrappelliSortableHiddenMixin
from .models import Group, Term, Event, Form, FormField, Sheet, SheetColumn

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'site')
    list_filter = ('site__name',)
    search_fields = ('name', 'code')
    prepopulated_fields = { 'slug': ('code',), 'sort': ('code',) }



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



class SheetColumnInline(GrappelliSortableHiddenMixin, admin.StackedInline):
    model = SheetColumn
    sortable_field_name = 'position'

@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    inlines = [SheetColumnInline]
