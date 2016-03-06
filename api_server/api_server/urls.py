from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views import defaults
from django.views.generic import TemplateView

admin.autodiscover()
admin.site.login = defaults.permission_denied

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'api_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^people/', include('people.urls')),
    url(r'^packages/', include('packages.urls')),
    url(r'^guestlist/', include('guestlist.urls')),
    url(r'^sevenk/', include('sevenk.urls')),
    url(r'^rooming/', include('rooming.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^403$', TemplateView.as_view(template_name="403.html")),
)
