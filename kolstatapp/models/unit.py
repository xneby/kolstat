# coding: utf-8
from django.db import models

UNIT_CATEGORIES = (("EL", "Electric Locomotive"), ("DL", "Diesel Locomotive"), ("EMU", "Electric Multiple Unit"), ("DMU", "Diesel Multiple Unit"), ("C", "Carriage"))

class UnitClass(models.Model):
	""" Typ/seria pojazdu trakcyjnego / wagonu """
	name = models.CharField(max_length = 50)
	category = models.CharField(choices = UNIT_CATEGORIES, max_length = 5)
	producer = models.CharField(max_length = 250)

	description = models.TextField(blank = True)

	class Meta:
		app_label = 'kolstatapp'
		verbose_name = 'Seria'
		verbose_name_plural = 'Serie'

	def __unicode__(self):
		return u"{self.name}".format(self = self)

class Unit(models.Model):
	""" Pojazd """
	name = models.CharField(max_length = 50)
	evn = models.TextField(blank = True)
	unitclass = models.ForeignKey('kolstatapp.UnitClass')
	producer = models.CharField(max_length = 250)
	yearofbuild = models.IntegerField()
	operator = models.ForeignKey('kolstatapp.Operator')
	depot = models.TextField(max_length = 100)

	description = models.TextField(blank = True)

	class Meta:
		app_label = 'kolstatapp'
		verbose_name = 'Pojazd'
		verbose_name_plural = 'Pojazdy'

	def __unicode__(self):
		return u"{self.name} ({self.evn})".format(self=self)
