from django import template
from django.conf import settings
from kolstatapp.models import Station

register = template.Library()

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
	
	if isinstance(station, Station):
		return station.get_pretty_name()
	
	try:
		return Station.objects.get(hafasID = station.externalId).get_pretty_name()
	except Station.DoesNotExist:
		return station.name
	except AttributeError:
		return ''
