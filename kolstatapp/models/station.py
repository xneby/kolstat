# -*- coding: utf-8 -*-
from django.db import models
from kolstatapp.utils.hafas import Hafas, HafasStation

STATION_CATEGORIES = (("M", "Main"), ("N", "Normal"))

class Station(models.Model):
	""" Stacja :) """
	name = models.CharField(max_length = 100)
	pretty_name = models.CharField(max_length = 100, null = True)
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
		for x in ('name__iexact', 'pretty_name__iexact', 'hafasID', 'kurs90ID'):
			try:
				model = cls.objects.get(**{x: query})
			except (cls.DoesNotExist, ValueError) as e:
				pass
			else:
				return [model]

#		hafasOutput = Hafas.searchStation(query.encode('utf-8'))
#		
#		result = []
#
#		for station in hafasOutput:
#			try:
#				model = cls.objects.get(hafasID = station.externalId)
#			except cls.DoesNotExist:
#				pass
#			else:
#				result.append(model)

		print 'search failed for', query

		return []

	def toHafas(self):
		return HafasStation(self.name, self.hafasID, (self.xCoord, self.yCoord))

	class Meta:
		app_label = 'kolstatapp'
		verbose_name = 'Stacja'
		verbose_name_plural = 'Stacje'

	def __unicode__(self):
		return u"{self.name} ({self.hafasID}, {self.kurs90ID})".format(self = self)
