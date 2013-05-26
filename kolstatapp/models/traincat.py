# coding: utf-8
from django.db import models
from django.conf import settings

class TrainType:
	LOCAL = 1
	FAST = 2
	EXPRESS = 3
	SUBURBAN = 4

	DICT = {
		LOCAL: "os",
		FAST: "posp",
		EXPRESS: "ex",
		SUBURBAN: "skm",
			}

	@classmethod
	def get_choices(cls):
		return (
			(cls.SUBURBAN, "Podmiejski"),
			(cls.LOCAL, "Osobowy"),
			(cls.FAST, "Pospieszny"),
			(cls.EXPRESS, "Ekspres"),
				)

	@classmethod
	def get_class(cls, num):
		return cls.DICT[num]

class Operator(models.Model):
	name = models.CharField(max_length = 100)
	website = models.URLField(null = True)
	has_description = models.BooleanField()

	def __str__(self):
		return self.name

	class Meta:
		app_label = 'kolstatapp'
		verbose_name = 'Przewoźnik'
		verbose_name_plural = 'Przewoźnicy'

class TrainCategory(models.Model):
	name = models.CharField(max_length = 10)
	full_name = models.CharField(max_length = 50)
	pic_name = models.CharField(max_length = 20)
	type = models.IntegerField(choices = TrainType.get_choices())
	operator = models.ForeignKey(Operator)

	def get_type_class(self):
		return TrainType.get_class(self.type)

	def url(self):
		return '{}img/traincat/{}.svg'.format(settings.STATIC_URL, self.pic_name)

	def __str__(self):
		return self.name

	class Meta:
		app_label = 'kolstatapp'
		verbose_name = 'Kategoria pociągu'
		verbose_name_plural = 'Kategorie pociągu'
