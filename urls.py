from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.conf import settings
#from utils import lazy_reverse

from django.core.urlresolvers import reverse
from django.utils.functional import lazy

from django.contrib import admin

lazy_reverse = lazy(reverse, str)

handler404 = 'kolstat.website.views.page_not_found'
handler500 = 'kolstat.website.views.server_error'

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^kolstat/', include('kolstatapp.urls')),

	url(r'^$', RedirectView.as_view(url = lazy_reverse('kolstat-home'), permanent = True)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

	url(r'^accounts/', include('allauth.urls')),

)
