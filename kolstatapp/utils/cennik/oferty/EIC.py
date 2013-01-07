from base import Oferta, Discounts, TICKET, SEAT

from kolstatapp.models import TrainCategory, Operator

class EICOferta(Oferta):
	name = 'EIC/Ex - Normalny'
	valid_discounts = Discounts.ustawowe + Discounts.IC

	EIC = TrainCategory.objects.get(name = 'EIC')
	Ex  = TrainCategory.objects.get(name = 'EX')

	operator = Operator.objects.get(name = 'PKP Intercity')

	distances = (
		(40,   35),
		(60,   43),
		(80,   50),
		(100,  55),
		(120,  65),
		(140,  71),
		(160,  75),
		(180,  82),
		(200,  86),
		(220,  90),
		(240,  93),
		(260,  98),
		(280,  103),
		(320,  114),
		(360,  117),
		(440,  119),
		(520,  121),
		(600,  123),
		(680,  132),
		(760,  135),
		(880,  138),
		(1000, 140),
	)

	@classmethod
	def is_valid(cls, train, start, end):
		return train.category in (cls.EIC, cls.Ex)

	@classmethod
	def _get_additional_prices(cls, train, disccount):
		return [(SEAT, 13.00, None)]
