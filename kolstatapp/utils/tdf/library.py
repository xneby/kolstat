# coding: utf-8
import yaml

from datetime import timedelta, time

from kolstatapp.models import Train, TrainCategory, TrainTimetable, Station, TrainStop, TrainCouple
from kolstatapp.utils.gsk.dijkstra import Dijkstra

def time_from_yaml(t):
	if t is None:
		return None

	if type(t) in (type(u'00:00'), type('00:00')):
		h, m = map(int, t.split(':'))
		t = 60*h+m
		
	return time(minute = t % 60, hour = t // 60)

def import_train(yaml, mode):
	train = Train()

	name = yaml['name']
	category, number = name.split(' ')

	try:
		t, = train.search(name)
	except ValueError:
		pass
	else:
		print "Już było"
		if mode == 'force' or True:
			print 'Usuwam'
			t.delete()
		else:
			return


	train.category = TrainCategory.objects.get(name = category)
	train.number = number
	train.variant = 'A'

	train.save()

	operations = yaml['operations']

	service = {}

	for oper in operations:
		if oper['mode'] == 'interval':
			start = oper['from']
			end = oper['to']

			service[end] = oper['timetable']

			while start != end:
				service[start] = oper['timetable']
				start += timedelta(days = 1)

		elif oper['mode'] == 'single':
			date = oper['date']
			service[date] = oper['timetable']

	stops = []

	for date, timetable in service.items():
		print date
		tt = TrainTimetable(train = train, date = date)
		tt.save()

		i = 1
		prev = None
		arr_over = False

		for description in timetable:
			stop = TrainStop(timetable = tt)
			stop.station = Station.search(description['station'])[0]
			stop.departure = time_from_yaml(description.get('departure', None))
			stop.arrival = time_from_yaml(description.get('arrival', None))
			stop.order = i

			if prev is not None:
				if arr_over or stop.arrival < prev.departure:
					stop.arrival_overnight = 1
					arr_over = True
			
			if arr_over or (stop.arrival is not None and stop.departure is not None and stop.arrival > stop.departure):
				stop.departure_overnight = 1
				arr_over = True

			if prev is None:
				stop.distance = 0.0
			else:
				stop.distance = prev.distance + Dijkstra.length(prev.station.gskID, stop.station.gskID)

			prev = stop

			stops.append(stop)

			i += 1
		if arr_over:
			print 'arr_over!'

	TrainStop.objects.bulk_create(stops)

def import_couple(yaml, mode):
	for field in ('station', 'trains'):
		if field not in yaml:
			raise ValueError('Zły yaml - brak "{field}"'.format(field = field))

	trains = yaml['trains']
	station_name = yaml['station']
	
	(t1 ,), (t2 ,) = map(Train.search, trains)
	s, = Station.search(station_name)

	print t1, t2

	to_add = []

	for tt in t1.timetables():
		try:
			st = tt.stops().get(station = s)
		except TrainStop.DoesNotExist:
			continue
		try:
			st2 = t2.timetables().get(date = tt.date).stops().get(station = s)
		except TrainTimetable.DoesNotExist, TrainStop.DoesNotExist:
			continue

		print tt.date

		to_add.append(TrainCouple(stop1 = st2, stop2 = st))
		to_add.append(TrainCouple(stop1 = st, stop2 = st2))

	TrainCouple.objects.bulk_create(to_add)

importers = {
	'train': import_train,
	'couple': import_couple,
}

def import_from_file(s):
	doc = yaml.load(s)

	if doc['type'] not in importers:
		raise ValueError('Nieobsługiwany typ')
	if 'mode' in doc:
		mode = doc['mode']
	else:
		mode = 'normal'
		
	importers[doc['type']](doc, mode)
	
