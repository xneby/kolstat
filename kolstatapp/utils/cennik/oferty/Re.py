from .base import Oferta, Discounts, TICKET, SEAT

from kolstatapp.models import TrainCategory, Operator

class ReOferta(Oferta):
	name = 'RegioEkspres - Normalny'
	valid_discounts = Discounts.ustawowe + Discounts.R

	Re = TrainCategory.objects.get(name = 'RE')

	operator = Operator.objects.get(name = 'Przewozy Regionalne')

	distances = (
		(40,  12.00),
		(59,  16.90),
		(80,  20.90),
		(100, 24.90),
		(120, 31.90),
		(140, 36.90),
		(160, 40.90),
		(180, 43.90),
		(200, 46.90),
		(220, 49.90),
		(240, 51.90),
		(260, 53.90),
		(280, 55.90),
		(320, 59.90),
		(360, 62.90),
		(400, 64.90),
		(500, 66.90),
		(600, 70.90),
		(700, 75.90),
		(800, 79.90),
	)

	@classmethod
	def is_valid(cls, train, start, end):
		return train.category == cls.Re

	@classmethod
	def get_additional_prices(cls, train, disccount):
		return []

