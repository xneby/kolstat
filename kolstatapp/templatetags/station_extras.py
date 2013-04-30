from django import template
from django.conf import settings
from kolstatapp.models import Station

from django.core.urlresolvers import reverse

register= template.Library()

@register.simple_tag
def get_class_if_main(station):
	try:
		st = Station.objects.get(hafasID = station.externalId)
		if st.category == 'M':
			return ' station-main'
		else:
			return ''

	except Station.DoesNotExist:
		return ''

@register.simple_tag
def kurs90(station):
	try:
		st = Station.objects.get(hafasID = station.externalId)
		return st.kurs90ID
	except Station.DoesNotExist:
		return ''

@register.simple_tag
def gskID(station):
	try:
		st = Station.objects.get(hafasID = station.externalId)
		return st.gskID
	except Station.DoesNotExist:
		return ''

@register.simple_tag
def get_pretty_name(station):
	def _get_pretty_name(station):
	
		if isinstance(station, Station):
			return station
	
		try:
			return Station.objects.get(hafasID = station.externalId)
		except Station.DoesNotExist:
			return station.name
		except AttributeError:
			return None
	st = _get_pretty_name(station)
	if st is None:
		return '###ARG!'
	return '<span class="station"><a href="{}">{}</a></span>'.format(reverse('kolstat-station-show', args = [st.slug]), st.get_pretty_name())
