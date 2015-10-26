from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Member, Contact, RSVP

class BirthYearListFilter(admin.SimpleListFilter):
    title = _(u"Birthyear")
    parameter_name = 'birthyear'
    
    def lookups(self, request, model_admin):
        years = model_admin.get_queryset(request).dates('birthday', 'year')
        return [ (year.year, year.year) for year in years ]
    
    def queryset(self, request, queryset):
        return queryset

class RSVPInline(admin.StackedInline):
    model = RSVP

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birthday', 'site')
    list_filter = ('group', BirthYearListFilter, 'site__name')
    search_fields = ('first_name', 'last_name')
    inlines = [RSVPInline]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'site')
    list_filter = ('site__name',)
    search_fields = ('first_name', 'last_name')
