from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib import messages

class RedirectIncompleteMiddleware(object):
    required_keys = ['email', 'first_name', 'last_name']
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Ignore logged-out users, they obviously can't be complete
        if request.user.is_authenticated():
            
            # Ignore requests to the settings page; we don't want redirect loops
            m = request.resolver_match
            if not m or m.url_name != 'account_settings':
                
                # Redirect users with missing profile info to the settings page
                for key in self.required_keys:
                    if not getattr(request.user, key):
                        messages.add_message(request, messages.INFO,
                            _(u"Please complete your profile before proceeding!"))
                        return redirect(reverse('account_settings'))
