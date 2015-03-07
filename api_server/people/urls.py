from django.conf.urls import patterns, include, url
from django.contrib import admin
import people.views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^full$', 'people.views.full'),
    url(r'^profile/(?P<username>\w+)$', people.views.Profile.as_view()),
)
