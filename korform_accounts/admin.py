from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from .models import User, Profile

class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    
    def get_fieldsets(self, *args, **kwargs):
        data = super(BaseUserAdmin, self).get_fieldsets(*args, **kwargs)
        l = list(data)
        l.insert(2, (u"Profile", {
            'fields': ('profile',),
        }))
        return tuple(l)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
