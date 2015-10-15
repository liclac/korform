from django.contrib import admin
from grappelli.forms import GrappelliSortableHiddenMixin
from .models import Term, Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

class EventInline(GrappelliSortableHiddenMixin, admin.StackedInline):
    model = Event
    sortable_field_name = 'position'

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    inlines = [EventInline]
