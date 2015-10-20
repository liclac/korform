from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Member, RSVP

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
    list_display = ('first_name', 'last_name', 'birthday')
    list_filter = ('group', BirthYearListFilter)
    search_fields = ('first_name', 'last_name')
    inlines = [RSVPInline]
