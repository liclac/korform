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



def profile_users(profile):
    items = profile.users.values_list('first_name', 'last_name')
    names = [u"{0} {1}".format(i[0], i[1]) for i in items]
    return u", ".join(names)
profile_users.short_description = u"Users"

def profile_members(profile):
    items = profile.members.values_list('first_name', 'last_name')
    names = [u"{0} {1}".format(i[0], i[1]) for i in items]
    return u", ".join(names)
profile_members.short_description = u"Members"

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (profile_users, profile_members)
