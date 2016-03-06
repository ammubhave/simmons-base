from django.conf.urls import patterns, include, url
from django.contrib import admin
import packages.views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^notify$', packages.views.PackageNotify.as_view()),
)
