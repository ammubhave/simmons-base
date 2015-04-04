from django.conf.urls import patterns, include, url
from django.contrib import admin
import sevenk.views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^taken$', 'rooming.views.taken'),
    url(r'^occupants$', 'rooming.views.occupants'),
    #url(r'^profile/(?P<username>\w+)$', people.views.Profile.as_view()),
    url(r'^run_randomization$', 'rooming.views.run_randomization'),
)
