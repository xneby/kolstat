from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.conf import settings
#from utils import lazy_reverse

from django.core.urlresolvers import reverse
from django.utils.functional import lazy

from django.contrib import admin

lazy_reverse = lazy(reverse, str)

handler404 = 'kolstat.website.views.page_not_found'
handler500 = 'kolstat.website.views.server_error'

dajaxice_autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^kolstat/', include('kolstatapp.urls')),
	url(r'^$', redirect_to, {'url': lazy_reverse('kolstat-home'), 'permament': True}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

	url(r'external/', include('social_auth.urls')),
	
	url(r'accounts/logged/', redirect_to, {'url': '/kolstat/profile/'} ),
	url(r'accounts/login/', 'django.contrib.auth.views.login', {'template_name': 'user/login.html'} , name= 'django-login'),
	url(r'accounts/logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}, name= 'django-logout'),

	url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)
