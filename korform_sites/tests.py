from django.test import TestCase
from django.contrib.sites.models import Site
from .models import SiteConfig

class TestSiteConfig(TestCase):
    def setUp(self):
        self.site = Site.objects.create(domain=u"google.com", name=u"Google")
    
    def test_config_created(self):
        '''Newly created Sites should have an associated SiteConfig.'''
        self.assertIsNotNone(self.site.config)
