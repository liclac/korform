from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name

class CustomIndexDashboard(Dashboard):
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        self.children.append(modules.ModelList(
            u"Authentication and Authorization",
            column=1,
            collapsible=False,
            models=(
                'korform_accounts.models.Profile',
                'korform_accounts.models.User',
                'korform_accounts.models.InviteKey',
                'django.contrib.auth.models.Group',
                'registration.models.RegistrationProfile',
            )
        ))
        
        self.children.append(modules.ModelList(
            u"Sites",
            column=1,
            collapsible=False,
            models=(
                'django.contrib.sites.models.*',
                'korform_sites.models.*',
                'django.contrib.flatpages.models.*',
            )
        ))
        
        self.children.append(modules.ModelList(
            u"Planning",
            column=1,
            collapsible=False,
            models=(
                'korform_planning.models.Term',
                'korform_planning.models.Group',
                'korform_planning.models.Form',
                'korform_planning.models.Sheet',
                'korform_planning.models.*',
            )
        ))
        
        self.children.append(modules.ModelList(
            u"Roster",
            column=1,
            collapsible=False,
            models=(
                'korform_roster.models.Member',
                'korform_roster.models.Contact',
                'korform_roster.models.*',
            )
        ))
        
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            column=2,
            collapsible=False,
            limit=5,
        ))
