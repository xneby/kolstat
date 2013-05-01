# -*- coding: utf-8 -*-
from django.db import models
import operator
from functools import reduce
import datetime

STATION_CATEGORIES = (("M", "Main"), ("N", "Normal"))

class Station(models.Model):
	""" Stacja :) """
	name = models.CharField(max_length = 100)
	pretty_name = models.CharField(max_length = 100, null = True)
	slug = models.SlugField(max_length = 100, null = True)

	hafasID = models.IntegerField(unique = True, null = True)
	kurs90ID = models.IntegerField(unique = True, null = True)
	gskID = models.IntegerField(unique = True, null = True)

	category = models.CharField(choices = STATION_CATEGORIES, max_length = 3)

	xCoord = models.IntegerField(null = True)
	yCoord = models.IntegerField(null = True)

	def get_pretty_name(self):
		if self.pretty_name is None:
			return self.name
		return self.pretty_name

	@classmethod
	def search(cls, query):
		"""Zwraca listę stacji o {nazwie, id} == query lub jeśli takie nie
		istnieją wykonuje zapytanie do Hafasa
		"""

		require_str = reduce(operator.or_, (models.Q(**{x: query}) for x in ('name__iexact', 'pretty_name__iexact', 'slug__iexact')))
		require_num = reduce(operator.or_, (models.Q(**{x: query}) for x in ('hafasID', 'kurs90ID')))
		if type(query) == type(0) or query.isdigit():
			require = require_num
		else:
			require = require_str
#		print require
		return cls.objects.filter(require).all()
			
		print('search failed for', query)

		return []

#	def toHafas(self):
#		return HafasStation(self.name, self.hafasID, (self.xCoord, self.yCoord))

	def next_departures(self, number):
		tomorrow = datetime.date.today() + datetime.timedelta(days = 1)
		all_stops = self.trainstop_set.filter(timetable__date__lte = tomorrow).filter(timetable__date__gte = datetime.date.today()).exclude(departure = None)

		return list(x for x in sorted(all_stops, key = lambda x : x.departure_datetime()) if x.departure_datetime() > datetime.datetime.now() )[:5]

	class Meta:
		app_label = 'kolstatapp'
		verbose_name = 'Stacja'
		verbose_name_plural = 'Stacje'

	def __str__(self):
		return "{self.name} ({self.hafasID}, {self.kurs90ID})".format(self = self)

	def to_json(self):
		return dict(id = self.id, name = self.get_pretty_name(), slug = self.slug)
