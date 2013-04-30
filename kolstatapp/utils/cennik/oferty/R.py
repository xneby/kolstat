from .base import Oferta, Discounts, TICKET, SEAT

from kolstatapp.models import TrainCategory, Operator

class ROferta(Oferta):
	name = 'Regio - Normalny'
	valid_discounts = Discounts.ustawowe + Discounts.R

	R = TrainCategory.objects.get(name = 'R')

	operator = Operator.objects.get(name = 'Przewozy Regionalne')

	distances = (
		(5,   4.00),
		(10,  4.40),
		(15,  5.30),
		(20,  6.50),
		(25,  7.60),
		(30,  8.20),
		(40,  10.60),
		(47,  11.70),
		(53,  13.50),
		(59,  14.60),
		(67,  15.60),
		(73,  16.10),
		(80,  17.10),
		(90,  18.60),
		(100, 19.80),
		(120, 22.00),
		(140, 23.60),
		(160, 25.50),
		(180, 27.10),
		(200, 29.10),
		(240, 31.20),
		(280, 33.30),
		(320, 35.40),
		(360, 37.10),
		(400, 39.00),
		(500, 41.00),
		(600, 43.00),
		(700, 45.00),
		(800, 47.00),
	)

	@classmethod
	def is_valid(cls, train, start, end):
		return train.category == cls.R

	@classmethod
	def get_additional_prices(cls, train, disccount):
		return []

