from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'sdb.views.home', name='home'),
    url(r'^profile/$', 'sdb.views.my_profile', name='my_profile'),
    url(r'^profile/(?P<username>[a-zA-Z0-9]+)$', 'sdb.views.view_profile', name='view_profile'),
    url(r'^officers/$', 'sdb.views.officers', name='officers'),
    url(r'^govtracker/$', 'sdb.views.govtracker_home', name='govtracker_home'),

    url(r'^messenger_callback', 'sdb.views.messenger_callback'),
    url(r'^admin/', include(admin.site.urls)),
)
