# coding: utf-8
import yaml

from datetime import timedelta, time, datetime

from kolstatapp.models import Train, TrainCategory, TrainTimetable, Station, TrainStop, TrainCouple
from kolstatapp.utils.gsk.dijkstra import Dijkstra

import threading

from django.db import connection, transaction

DZIEN = timedelta(days = 1)

def time_from_yaml(t):
	if t is None:
		return None

	if type(t) in (type('00:00'), type('00:00')):
		h, m = list(map(int, t.split(':')))
		t = 60*h+m
		
	return time(minute = t % 60, hour = t // 60)

def import_train(yaml, mode, dijkstra_lock, mysql_lock):
	train = Train()

	name = yaml['name']
	category, number = name.split(' ')

	try:
		with mysql_lock:
			t, = train.search(name, variant = yaml['variant'])
	except ValueError:
		pass
	else:
		if mode == 'force' or True:
			t.delete()
		else:
			return


	with mysql_lock:
		train.category = TrainCategory.objects.get(name = category)
	
	train.number = number
	train.variant = yaml['variant']

	with mysql_lock:
		train.save()

	operations = yaml['operations']

	for oper in operations:
		if oper['mode'] == 'interval':
			start = oper['from']
			end = oper['to']
			dates = [ end ]
			while start != end:
				dates.append(start)
				start += DZIEN
		elif oper['mode'] == 'single':
			dates = [ oper['date'] ]
		elif oper['mode'] == 'multi':
			dates = oper['dates']

		timetable = oper['timetable']
		
		tts = []
		for i in dates:
			tts.append(TrainTimetable(train = train, date =i))
		
		with mysql_lock:
			TrainTimetable.objects.bulk_create(tts)

		tts = train.traintimetable_set.all()
		ttbd = {}

		for x in tts:
			ttbd[x.date] = x

		stops = []

		tt = ttbd[dates[0]]

		i = 1
		prev = None
		arr_over = False

		for description in timetable:
			stop = TrainStop(timetable = tt)
			try:
				stop.station = Station.search(description['station'])[0]
			except IndexError:
				print(description)
				raise
			if 'departure' in description:
				stop.departure = datetime.combine(tt.date, time_from_yaml(description.get('departure', None)))
			if 'arrival' in description:
				stop.arrival = datetime.combine(tt.date, time_from_yaml(description.get('arrival', None)))
			stop.track = description.get('track', None)
			stop.platform = description.get('platform', None)
			stop.order = i

			if prev is not None:
				if arr_over or stop.arrival < prev.departure:
#					stop.arrival_overnight = 1
					arr_over = True
			
			if arr_over or (stop.arrival is not None and stop.departure is not None and stop.arrival > stop.departure):
#				stop.departure_overnight = 1
				arr_over = True

			if prev is None:
				stop.distance = 0.0
			else:
				dijkstra_lock.acquire()
				stop.distance = prev.distance + Dijkstra.length(prev.station.gskID, stop.station.gskID)
				dijkstra_lock.release()

			prev = stop

			stops.append(stop)

			i += 1

		with mysql_lock:
			TrainStop.objects.bulk_create(stops)

		cursor = connection.cursor()

		for d, tt in ttbd.items():
			if d == dates[0]: continue
			tto = ttbd[dates[0]]
			ttn = ttbd[d]

			with mysql_lock:
				cursor.execute(''' INSERT INTO kolstatapp_trainstop (timetable_id, station_id, arrival, departure, track, platform, distance, "order") SELECT {0}, station_id, arrival + '{2} days', departure + '{2} days', track, platform, distance, "order" FROM kolstatapp_trainstop WHERE timetable_id = {1}'''.format(ttn.pk, tto.pk, (d - dates[0]).days))

		with mysql_lock:
			transaction.commit_unless_managed()


def import_couple(yaml, mode):
	for field in ('station', 'trains'):
		if field not in yaml:
			raise ValueError('Zły yaml - brak "{field}"'.format(field = field))

	trains = yaml['trains']
	station_name = yaml['station']
	
	(t1 ,), (t2 ,) = list(map(Train.search, trains))
	s, = Station.search(station_name)

	print(t1, t2)

	to_add = []

	for tt in t1.timetables():
		try:
			st = tt.stops().get(station = s)
		except TrainStop.DoesNotExist:
			continue
		try:
			st2 = t2.timetables().get(date = tt.date).stops().get(station = s)
		except TrainTimetable.DoesNotExist as xxx_todo_changeme:
			TrainStop.DoesNotExist = xxx_todo_changeme
			continue

		print(tt.date)

		to_add.append(TrainCouple(stop1 = st2, stop2 = st))
		to_add.append(TrainCouple(stop1 = st, stop2 = st2))

	TrainCouple.objects.bulk_create(to_add)

importers = {
	'train': import_train,
	'couple': import_couple,
}

def import_from_file(s, dijkstra_lock, mysql_lock):
	doc = yaml.load(s)

	if doc['type'] not in importers:
		raise ValueError('Nieobsługiwany typ')
	if 'mode' in doc:
		mode = doc['mode']
	else:
		mode = 'normal'
		
	importers[doc['type']](doc, mode, dijkstra_lock, mysql_lock)
	
