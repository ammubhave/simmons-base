from django.conf.urls import patterns, include, url
from django.contrib import admin
import people.views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^full$', 'people.views.full'),
    url(r'^medlinks$', 'people.views.medlinks'),
    url(r'^grts$', 'people.views.grts'),
    url(r'^profile/(?P<username>\w+)$', people.views.Profile.as_view()),
    url(r'^fifteen_seconds_of_frame$', 'people.views.get_fifteen_seconds_of_frame'),
    url(r'^me$', 'people.views.me'),
)
