from .base import Oferta, Discounts, TICKET, SEAT

from kolstatapp.models import TrainCategory, Operator

class EICOferta(Oferta):
	name = 'EIC/Ex - Normalny'
	valid_discounts = Discounts.ustawowe + Discounts.IC

	EIC = TrainCategory.objects.get(name = 'EIC')
	Ex  = TrainCategory.objects.get(name = 'EX')

	operator = Operator.objects.get(name = 'PKP Intercity')

	distances = (
		(40,   35+13),
		(60,   43+13),
		(80,   50+13),
		(100,  55+13),
		(120,  65+13),
		(140,  71+13),
		(160,  75+13),
		(180,  82+13),
		(200,  86+13),
		(220,  90+13),
		(240,  93+13),
		(260,  98+13),
		(280,  103+13),
		(320,  114+13),
		(360,  117+13),
		(440,  119+13),
		(520,  121+13),
		(600,  123+13),
		(680,  132+13),
		(760,  135+13),
		(880,  138+13),
		(1000, 140+13),
	)

	@classmethod
	def is_valid(cls, train, start, end):
		return train.category in (cls.EIC, cls.Ex)

	@classmethod
	def _get_additional_prices(cls, train, disccount):
		return [(SEAT, 0.00, None)]
