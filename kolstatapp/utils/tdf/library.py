# coding: utf-8
import yaml

from datetime import timedelta, time

from kolstatapp.models import Train, TrainCategory, TrainTimetable, Station, TrainStop, TrainCouple
from kolstatapp.utils.gsk.dijkstra import Dijkstra

import threading

from django.db import connection, transaction

dijkstra_lock = threading.Lock()
mysql_lock = threading.Lock()
DZIEN = timedelta(days = 1)

def time_from_yaml(t):
	if t is None:
		return None

	if type(t) in (type('00:00'), type('00:00')):
		h, m = list(map(int, t.split(':')))
		t = 60*h+m
		
	return time(minute = t % 60, hour = t // 60)

def import_train(yaml, mode):
	global dijkstra_lock

	train = Train()

	name = yaml['name']
	category, number = name.split(' ')

	try:
		t, = train.search(name, variant = yaml['variant'])
	except ValueError:
		pass
	else:
		if mode == 'force' or True:
			t.delete()
		else:
			return


	train.category = TrainCategory.objects.get(name = category)
	train.number = number
	train.variant = yaml['variant']

	train.save()

	operations = yaml['operations']

	for oper in operations:
		if oper['mode'] == 'interval':
			start = oper['from']
			end = oper['to']

		elif oper['mode'] == 'single':
			start = oper['date']
			end = oper['date']
			service[date] = oper['timetable']

		timetable = oper['timetable']
		
		tts = []
		tts.append(TrainTimetable(train = train, date = end))
		nstart = start
		while nstart != end:
			tts.append(TrainTimetable(train = train, date = nstart))
			nstart += DZIEN

		TrainTimetable.objects.bulk_create(tts)

		tts = train.traintimetable_set.all()
		ttbd = {}

		for x in tts:
			ttbd[x.date] = x

		stops = []

		tt = ttbd[start]

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
				dijkstra_lock.acquire()
				stop.distance = prev.distance + Dijkstra.length(prev.station.gskID, stop.station.gskID)
				dijkstra_lock.release()

			prev = stop

			stops.append(stop)

			i += 1

		TrainStop.objects.bulk_create(stops)

		cursor = connection.cursor()

		while start != end:
			tto = ttbd[start]
			ttn = ttbd[end]

			with mysql_lock:
				cursor.execute(''' INSERT INTO kolstatapp_trainstop SELECT NULL, {}, station_id, arrival, departure, arrival_overnight, departure_overnight, distance, `order` FROM kolstatapp_trainstop WHERE timetable_id = {}'''.format(ttn.pk, tto.pk))

			end -= DZIEN
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

def import_from_file(s):
	doc = yaml.load(s)

	if doc['type'] not in importers:
		raise ValueError('Nieobsługiwany typ')
	if 'mode' in doc:
		mode = doc['mode']
	else:
		mode = 'normal'
		
	importers[doc['type']](doc, mode)
	
