from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views import defaults

admin.autodiscover()
admin.site.login = defaults.permission_denied

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'api_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^people/', include('people.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
)
