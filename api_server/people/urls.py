from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^full$', 'people.views.full'),
)
