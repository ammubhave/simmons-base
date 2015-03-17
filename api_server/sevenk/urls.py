from django.conf.urls import patterns, include, url
from django.contrib import admin
import sevenk.views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^my_uploads$', 'sevenk.views.my_uploads'),
    url(r'^entry/(?P<username>\w+)$', sevenk.views.Entry.as_view()),
)
