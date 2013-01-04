from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from kolstatapp.decorators import admin_required

urlpatterns = patterns('kolstatapp.views',
    url(r'^$', 'home', name='kolstat-home'),
    url(r'^test/$', 'test', name='kolstat-test'),
	url(r'^trains/search/$', 'trainsearch', name='kolstat-trains-search'),
	url(r'^trains/(?P<operator>[A-Z]+)/(?P<number>\d+)/$', 'train', name='kolstat-train'),
	url(r'^trains/(?P<operator>[A-Z]+)/(?P<number>\d+)/(?P<variant>[A-Z])/$', 'train', name='kolstat-train-variant'),
	url(r'^trains/(?P<operator>[A-Z]+)/(?P<number>\d+)/(?P<date>\d{4}-\d{2}-\d{2})/$', 'train_date', name='kolstat-train-date'),
	url(r'^trains/(?P<operator>[A-Z]+)/(?P<number>\d+)/(?P<variant>[A-Z])/(?P<date>\d{4}-\d{2}-\d{2})/$', 'train_date', name='kolstat-train-date-variant'),

	url(r'journeys/add/$', 'journey_add', name='journey-add'),
	url(r'journeys/add/step/2/$', 'journey_add_step2', name='journey-add-step2'),
	url(r'journeys/add/step/3/$', 'journey_add_step3', name='journey-add-step3'),
    url(r'journeys/add/finitialize/', 'journey_add_finitialize', name='journey-add-finitialize'),
    url(r'journeys/add/end/', 'journey_add_end', name='journey-add-end'),

	url(r'profile/$', 'profile', name='user-profile'),
	url(r'profile/journeys/', 'journeys', name='user-journeys'),

	url(r'admin/$', admin_required(TemplateView.as_view(template_name = 'admin.html')), name = 'admin'),
	url(r'admin/trains/$', 'train_list', name='admin-trains'),
	url(r'admin/trains/add$', 'train_add', name='admin-add-train'),
	url(r'admin/trains/(?P<train_id>\d+)/delete/', 'train_delete', name='admin-train-delete'),

)
