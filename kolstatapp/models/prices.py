# coding: utf-8
from django.db import models

class Discount(models.Model):
	kurs90ID = models.IntegerField(verbose_name = 'Numer wg Kurs90')
	kurs90Name = models.CharField(max_length = 5, verbose_name = 'Skrót wg Kurs90')

	discount = models.IntegerField(verbose_name = 'Wartość zniżki w procentach')

	description = models.TextField(verbose_name = 'Nazwa zniżki')
	documentName = models.TextField(verbose_name = 'Nazwa dokumentu uprawniającego do ulgi')

	class Meta:
		app_label = 'kolstatapp'
		verbose_name = 'zniżka'
		verbose_name_plural = 'zniżki'

	@classmethod
	def get(cls, name):
		return cls.objects.get(kurs90Name = name)

	def ratio(self):
		return (100 - self.discount) / 100.0

	def __unicode__(self):
		return u"Zniżka {} ({}) - {}%".format(self.kurs90Name, self.description, self.discount)