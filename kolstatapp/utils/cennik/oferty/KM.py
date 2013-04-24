from .base import Oferta, Discounts, TICKET, SEAT

from kolstatapp.models import TrainCategory, Operator

class KMOferta(Oferta):
	name = 'KM - Normalny'
	valid_discounts = Discounts.ustawowe + Discounts.KM

	KM = TrainCategory.objects.get(name = 'KM')

	operator = Operator.objects.get(name = 'Koleje Mazowieckie')

	distances = (
		(5,   3.30),
		(10,  5.20),
		(15,  6.10),
		(20,  7.30),
		(30,  9.40),
		(40,  10.60),
		(50,  12.50),
		(60,  13.80),
		(70,  15.30),
		(80,  17.00),
		(90,  18.60),
		(100, 20.30),
		(120, 22.20),
		(140, 23.80),
		(160, 25.50),
		(180, 27.00),
		(200, 29.00),
		(220, 31.00),
		(240, 32.00),
		(260, 33.00),
		(280, 35.00),
		(320, 36.00),
		(360, 37.00),
		(400, 38.00),
		(440, 39.00),
		(480, 40.00),
		(520, 41.50),
	)

	@classmethod
	def is_valid(cls, train, start, end):
		return train.category == cls.KM

	@classmethod
	def get_additional_prices(cls, train, disccount):
		return []

