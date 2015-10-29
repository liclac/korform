from django.contrib.sites.models import Site
from django.db import models
from annoying.fields import AutoOneToOneField

class SiteConfig(models.Model):
    site = AutoOneToOneField(Site, related_name='config')
    
    term_member = models.CharField(max_length=20, blank=False, default=u"member", verbose_name=u"Term: Member", help_text=u"Your site's term for a member.")
    term_members = models.CharField(max_length=20, blank=False, default=u"members", verbose_name=u"Term: Members", help_text=u"Plural form of the above.")
    term_contact = models.CharField(max_length=20, blank=False, default=u"contact", verbose_name=u"Term: Contact", help_text=u"Your site's term for a contact.")
    term_contacts = models.CharField(max_length=20, blank=False, default=u"contacts", verbose_name=u"Term: Contacts", help_text=u"Plural form of the above.")
    
    current_term = models.ForeignKey('korform_planning.Term', related_name='current_for', null=True, blank=True, help_text=u"The current term determines which events need RSVPs, what information is required of members, etc.")
    contact_form = models.ForeignKey('korform_planning.Form', related_name='contact_form_for', null=True, blank=True, help_text=u"Determines any additional information requested of Contacts. Contacts are not tied to a term, but to the members sharing their profile.")

def clear_site_cache(instance, created, raw, **kwargs):
    Site.objects.clear_cache()

models.signals.post_save.connect(clear_site_cache, sender=SiteConfig, dispatch_uid='siteconfig_clear_cache')
