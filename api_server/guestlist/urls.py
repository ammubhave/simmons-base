from django.conf.urls import patterns, include, url
from django.contrib import admin
import guestlist.views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^u/(?P<username>\w+)$', guestlist.views.DeUser.as_view()),
    url(r'^me$', 'guestlist.views.me'),
)
