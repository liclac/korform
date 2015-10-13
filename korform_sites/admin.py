from django.contrib import admin
from .models import SiteConfig

@admin.register(SiteConfig)
class ConfigAdmin(admin.ModelAdmin):
    pass
