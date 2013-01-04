# -*- coding: utf-8 -*-
import datetime
from django.utils import simplejson
from django.core.urlresolvers import reverse
from dajaxice.decorators import dajaxice_register

from kolstatapp.models import Station
from kolstatapp.models import TrainName
from kolstatapp.utils.hafas import Hafas
from kolstatapp.utils.traincat import get_img_url

@dajaxice_register
def searchStation(request, name):
	stations = map(lambda x: (x.hafasID, x.name),
			Station.search(name))


	return simplejson.dumps(stations)

@dajaxice_register
def searchConnection(request, date, source, destination):
	def _(s):
		x = Station.search(s)
		if len(x) != 1:
			raise ValueError('Zła nazwa stacji')
		st, = x
		return st

	source = _(source)
	destination = _(destination)

	hafasSource, = Hafas.searchStation(str(source.hafasID))
	hafasDestination, = Hafas.searchStation(str(destination.hafasID))

	print date

	date = datetime.date(date[2], date[1]+1, date[0])

	print date

	cl = Hafas.searchConnectionsByDate(hafasSource, hafasDestination, date)

	result = []

	for c in cl:
		c.queryRelation()

		s, = c.sections
		t = s.train

		print s.departure.time
		print s.arrival.time

		data = {}
		data['category'] = t.type
		data['category_img'] = get_img_url(t)
		data['number'] = t.number
		data['operator'] = t.operator
		data['relation_departure'] = t.relation_source().name
		data['relation_arrival'] = t.relation_destination().name
		data['departure'] = s.departure.time.strftime('%H:%M')
		data['arrival'] = s.arrival.time.strftime('%H:%M')
		data['name'] = TrainName.getName(t)
		data['trainUrl'] = reverse("kolstat-train", kwargs = {'id':t.getId()})

		result.append(data)

	return simplejson.dumps(result)
