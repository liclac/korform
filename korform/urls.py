"""korform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import index
from korform_accounts.views import *
from korform_accounts.forms import *
from korform_planning.views import GroupView
from korform_roster.views import MemberView, MemberUpdateView

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^groups/(?P<slug>[-\w]+)/$', GroupView.as_view(), name='group'),
    url(r'^members/(?P<pk>[0-9]+)/$', MemberView.as_view(), name='member'),
    url(r'^members/(?P<pk>[0-9]+)/edit/$', MemberUpdateView.as_view(), name='member_edit'),
    url(r'^accounts/settings/$', SettingsView.as_view(), name='account_settings'),
    url(r'^accounts/register/$', RegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'registration/login.html', 'authentication_form': MyAuthenticationForm}, name='auth_login'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls), name='admin'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [ url(r'^__debug__/', include(debug_toolbar.urls)) ]
