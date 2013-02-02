# coding: utf-8

from pprint import pprint
from make_query import make_simple_query
from kolstatapp.utils.kolstat_time import hours

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

	def __unicode__(self):
		s = u'\tSection:\n'
		for field in ('source', 'destination', 'departure', 'arrival', 'duration', 'distance', 'average_velocity', 'train', 'timetable'):
			s += u'\t{}: {}\n'.format(field, getattr(self, field))
		s += u'\tstops:\n'
		for ss in self.stops:
			s += u'\t\t{}\n'.format(ss)
		return s + u'\n'

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

	def __unicode__(self):
		s = u'Connection:\n'
		for field in ('source', 'destination', 'departure', 'arrival', 'duration', 'distance', 'average_velocity'):
			s += u'{}: {}\n'.format(field, getattr(self, field))
		for ss in self.sections:
			s += unicode(ss)
		return s

def make_connection(x):
	return Connection(x)

def make_query(source, dest, when):
	ans = make_simple_query(source, dest, when)

	return [make_connection(x) for x in ans]
