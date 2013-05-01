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

	url(r'^profile/$', 'profile', name='user-profile'),
	url(r'^profile/change-name/$', 'change_name', name='user-change-name'),
	url(r'^profile/journeys/', 'journeys', name='user-journeys'),
	url(r'^profile/discounts/', 'discounts', name='user-discounts'),
	url(r'^profile/favourites/', 'favourites', name='user-favourites'),

	url(r'^admin/$', admin_required(TemplateView.as_view(template_name = 'admin.html')), name = 'admin'),
	url(r'^admin/trains/$', 'train_list', name='admin-trains'),
	url(r'^admin/trains/add$', 'train_add', name='admin-add-train'),
	url(r'^admin/trains/(?P<train_id>\d+)/delete/', 'train_delete', name='admin-train-delete'),

	url(r'^units/classes/', 'units_classes', name='units-classes'),
	url(r'^units/class/(?P<unitclass>[A-Za-z0-9]+)/', 'units_class', name='units-class'),
	#url(r'unit/(?P<unit>.+)/', 'unit', name='unit'),

	url(r'^plans/$', 'plans_list', name = 'kolstat-plans'),
	url(r'^plans/new/$', 'plans_new', name = 'kolstat-plans-new'),
	url(r'^plans/query/from=(?P<st_start>[-a-z]+)/to=(?P<st_end>[-a-z]+)/when=(?P<when>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})/$', 'plans_query', name = 'kolstat-plans-query'),
	url(r'^plans/(?P<connection_id>[0-9a-f]{22})/reiseplan/$', 'reiseplan', name = 'kolstat-reiseplan'),
	url(r'^plans/(?P<connection_id>[0-9a-f]{22})/json/$', 'get_plan_json', name = 'kolstat-plan-json'),

	url(r'^prices/(?P<connection_id>[0-9a-f]{22})/$', 'prices_show', name = 'kolstat-prices-show'),

	url(r'^stations/$', TemplateView.as_view(template_name = 'stations/list.html'), name = 'kolstat-stations'),
	url(r'^station/show/$', 'station_show', name = 'kolstat-station-show-post'),
	url(r'^station/(?P<station>[-a-z]+)/$', 'station_show', name = 'kolstat-station-show'),

	url(r'^ajax/station/$', 'ajax_station'),
	url(r'^ajax/favourites/$', 'ajax_favourites'),
)
