from django.contrib import admin
from django.contrib.sites.models import Site
from .models import SiteConfig

admin.site.unregister(Site)

class SiteConfigInline(admin.StackedInline):
    model = SiteConfig
    inline_classes = ('grp-collapse grp-open',)

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    inlines = [SiteConfigInline]
