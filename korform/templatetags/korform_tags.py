from textwrap import dedent
from django import template

register = template.Library()

@register.filter
def model_help(model):
    extra_help = {
        'django.contrib.sites.models.Site':
            u'''
            Sites define global behavior. A single installation can house multiple sites, with
            different sets of data associated (but sharing users!).
            
            The most important function of a Site is to define the current [term](/admin/korform_planning/term/),
            as well as the site title and the hostname used when sending links in emails.
            '''
    }
    
    help_text = getattr(model, '__help__', None)
    
    if not help_text:
        class_name = '.'.join([model.__class__.__module__, model.__class__.__name__])
        if class_name in extra_help:
            help_text = dedent(extra_help[class_name]).strip()
    
    return help_text
