from django.contrib import admin
from grappelli.forms import GrappelliSortableHiddenMixin
from .models import Group, Term, Event

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

class EventInline(GrappelliSortableHiddenMixin, admin.StackedInline):
    model = Event
    sortable_field_name = 'position'

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    inlines = [EventInline]
