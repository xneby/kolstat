from .base import Oferta, Discounts, TICKET, SEAT

from kolstatapp.models import TrainCategory, Operator

class iROferta(Oferta):
	name = 'InterRegio - Normalny'
	valid_discounts = Discounts.ustawowe + Discounts.R

	iR = TrainCategory.objects.get(name = 'IR')

	operator = Operator.objects.get(name = 'Przewozy Regionalne')

	distances = (
		(40,  11.00),
		(59,  14.90),
		(80,  18.90),
		(100, 22.90),
		(120, 27.90),
		(140, 31.90),
		(160, 33.90),
		(180, 36.90),
		(200, 38.90),
		(220, 43.90),
		(240, 46.90),
		(260, 47.90),
		(280, 49.90),
		(320, 53.90),
		(360, 56.90),
		(400, 59.90),
		(500, 61.90),
		(600, 65.90),
		(700, 69.90),
		(800, 73.90),
	)

	@classmethod
	def is_valid(cls, train, start, end):
		return train.category == cls.iR

	@classmethod
	def get_additional_prices(cls, train, disccount):
		return []

