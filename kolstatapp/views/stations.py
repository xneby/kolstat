from kolstatapp.decorators import expose
from kolstatapp.exceptions import Redirect
from kolstatapp.models import Station, TrainStop
from django.core.urlresolvers import reverse
import datetime

@expose('stations/show.html')
def station_show(request, station = None):
	if request.method == 'POST':
		if 'station' in request.POST:
			station = request.POST['station']
	
	if station is None:
		raise Redirect(reverse('kolstat-stations'))

	
	st = Station.search(station)
	if len(st) == 0 or len(st) > 1:
		raise Redirect(reverse('kolstat-stations'))

	st, = st

	stops = st.next_departures(5)

	return dict(station = st, stops = stops)
