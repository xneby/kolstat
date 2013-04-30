# coding: utf-8

from pprint import pprint
from .make_query import make_simple_query
from kolstatapp.utils.kolstat_time import hours
import pickle
import os
from django.conf import settings
import hashlib
import datetime

class Section(object):
	def __init__(self, stops):
		self.stops = stops

		self.source = stops[0].station
		self.destination = stops[-1].station

		self.departure = stops[0].departure_datetime()
		self.arrival = stops[-1].arrival_datetime()

		self.duration = hours(self.arrival - self.departure)
		self.distance = self.stops[-1].distance - self.stops[0].distance
		self.average_velocity = self.distance / self.duration

		self.train = stops[0].timetable.train
		self.timetable = stops[0].timetable

	def __str__(self):
		s = '\tSection:\n'
		for field in ('source', 'destination', 'departure', 'arrival', 'duration', 'distance', 'average_velocity', 'train', 'timetable'):
			s += '\t{}: {}\n'.format(field, getattr(self, field))
		s += '\tstops:\n'
		for ss in self.stops:
			s += '\t\t{}\n'.format(ss)
		return s + '\n'

class Transfer(object):
	def __init__(self, s1, s2):
		self.station = s1.station
		self.time = s2.departure_datetime() - s1.arrival_datetime()

class Connection(object):
	def __init__(self, el_conns):
		self.sections = []
		section = []
		for s1, s2 in el_conns:
			if section == [] or section[-1].timetable == s2.timetable:
				if section == []:
					section.append(s1)
				section.append(s2)
			else:
				self.sections.append(Section(section))
				section = [s1, s2]
		if section != []:
			self.sections.append(Section(section))

		self.source = self.sections[0].source
		self.destination = self.sections[-1].destination
		self.departure = self.sections[0].departure
		self.arrival = self.sections[-1].arrival
		self.distance = sum(s.distance for s in self.sections)
		self.duration = sum(s.duration for s in self.sections)

		self.average_velocity = self.distance / self.duration

		self.transfers = [Transfer(s1.stops[-1], s2.stops[0]) for s1, s2 in zip(self.sections, self.sections[1:])]

		for i in range(len(self.sections)-1):
			self.sections[i].transfer = self.transfers[i]

		self.save()

	def __str__(self):
		s = 'Connection:\n'
		for field in ('source', 'destination', 'departure', 'arrival', 'duration', 'distance', 'average_velocity'):
			s += '{}: {}\n'.format(field, getattr(self, field))
		for ss in self.sections:
			s += str(ss)
		return s

	def save(self):
		ss = pickle.dumps(self)
		
		cid = '{}{}'.format( datetime.datetime.now().strftime('%Y%m%d%H%M%S'), hashlib.sha1(ss).hexdigest()[:8])

		self.cid = cid
		file_name = settings.INSTALL_DIR + '/connection_cache/{}'.format(cid)
		with open(file_name, 'wb') as f:
			f.write(ss)

	@staticmethod
	def load(cid):
		file_name = settings.INSTALL_DIR + '/connection_cache/{}'.format(cid)
		if not os.access(file_name, 0):
			raise ValueError('Zły numer połączenia')
		with open(file_name, 'rb') as f:
			return pickle.load(f)

from itertools import chain, combinations

def subsets(iterable):
	s = list(iterable)
	return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def make_connection(x):
#	return Connection(x)
	def print_tt(s):
		print(s.train.category.name, s.train.number, s.first_stop().station.get_pretty_name(), s.last_stop().station.get_pretty_name())

	def get_last_transfer(tt1, tt2):
		qs = tt1.trainstop_set.filter(station_id__in = (tt2.get_stations_id())).order_by('-order')
		print_tt(tt1)
		print_tt(tt2)
		if qs:
			return qs[0].station
		return None

	tt = []
	for a, _ in x:
		if tt == [] or tt[-1] != a.timetable:
			tt.append(a.timetable)

	y = []
	
	start = x[0][0].station
	stop = x[-1][-1].station
	
	for ss in subsets(tt):
		if len(ss) == 0: continue
		if len(ss) > len(y) > 0: continue
		if not ss[0].trainstop_set.filter(station = start).exists(): continue
		if not ss[-1].trainstop_set.filter(station = stop).exists(): continue

		ok = True

		for p,n in zip(ss, ss[1:]):
			if get_last_transfer(p,n) is None:
				ok = False
				break

		if not ok:
			continue

		y = ss

	transfers = [start] + list(get_last_transfer(x,y) for x,y in zip(y,y[1:])) + [stop]

	for x in transfers:
		print(x.get_pretty_name())

	print(y)
	for x in y:
		print_tt(x)

	yy = []
	for tt, (s1, s2) in zip(y, zip(transfers, transfers[1:])):
		interval = tt.interval(s1,s2)
		yy.extend(zip(interval, interval[1:]))

	return Connection(yy)

def make_query(source, dest, when):
	ans = make_simple_query(source, dest, when)

	return [make_connection(x) for x in ans]
