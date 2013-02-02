# coding: utf-8
from base import Oferta, Discounts, TICKET, SEAT

from kolstatapp.models import TrainCategory, Operator, Station

class KMRadomPionki(Oferta):
	name = 'KM - Oferta specjalna (Radom - Pioni)'
	valid_discounts = Discounts.ustawowe + Discounts.KM

	KM = TrainCategory.objects.get(name = 'KM')

	operator = Operator.objects.get(name = 'Koleje Mazowieckie')

	valid_stations = (Station.objects.get(name = x) for x in ('Radom', 'Rajec Poduchowny', 'Antoniówka', 'Jedlnia Letnisko', 'Jedlnia Kościelna', 'Pionki Zach.', 'Pionki'))

	distances = (
		(15,  3.40),
		(25,  4.50),
	)

	@classmethod
	def is_valid(cls, train, start, end):
		return train.category == cls.KM and start.station in cls.valid_stations and end.station in cls.valid_stations

	@classmethod
	def get_additional_prices(cls, train, disccount):
		return []

