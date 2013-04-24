# coding: utf-8
from django.db import models

UNIT_CATEGORIES = (("EL", "Electric Locomotive"), ("DL", "Diesel Locomotive"), ("EMU", "Electric Multiple Unit"), ("DMU", "Diesel Multiple Unit"), ("C", "Carriage"))
PL_CATEGORIES_PLURAL = {"EL": "Lokomotywy elektryczne", "DL": "Lokomotywy spalinowe", "EMU": "Elektryczne zespoły trakcyjne", "DMU": "Spalinowe zespoły trakcyjne i szynobusy", "C": "Wagony"}
PL_CATEGORIES = {"EL": "lokomotywa elektryczna", "DL": "lokomotywa spalinowa", "EMU": "elektryczny zespół trakcyjny", "DMU": "spalinowy zespół trakcyjny/szynobus", "C": "wagon"}

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
		return "{self.name}".format(self = self)

	def get_polish_category_plural(self):
		return PL_CATEGORIES_PLURAL[self.category]
	def get_polish_category(self):
		return PL_CATEGORIES[self.category]

class Unit(models.Model):
	""" Pojazd """
	name = models.CharField(max_length = 50)
	evn = models.TextField(blank = True)
	unitclass = models.ForeignKey('kolstatapp.UnitClass')
	producer = models.CharField(max_length = 250)
	yearofbuild = models.IntegerField(blank = True)
	operator = models.ForeignKey('kolstatapp.Operator')
	depot = models.TextField(max_length = 100, blank = True)

	description = models.TextField(blank = True)

	class Meta:
		app_label = 'kolstatapp'
		verbose_name = 'Pojazd'
		verbose_name_plural = 'Pojazdy'

	def __unicode__(self):
		return "{self.name}".format(self=self)
