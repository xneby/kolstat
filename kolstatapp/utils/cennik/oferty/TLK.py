from base import Oferta, Discounts, TICKET, SEAT

from kolstatapp.models import TrainCategory, Operator

class TLKOferta(Oferta):
	name = 'TLK - Normalny'
	valid_discounts = Discounts.ustawowe + Discounts.IC

	TLK = TrainCategory.objects.get(name = 'TLK')

	operator = Operator.objects.get(name = 'PKP Intercity')

	distances = (
		(40,   13),
		(60,   19),
		(80,   23),
		(100,  26),
		(120,  37),
		(140,  40),
		(160,  42),
		(180,  44),
		(200,  47),
		(220,  50),
		(240,  52),
		(260,  54),
		(280,  56),
		(320,  60),
		(360,  62),
		(440,  65),
		(520,  67),
		(600,  69),
		(680,  73),
		(760,  78),
		(880,  80),
		(1000, 83),
	)

	seat_ticket = ('15117', )

	@classmethod
	def is_valid(cls, train, start, end):
		return train.category == cls.TLK

	@classmethod
	def _get_additional_prices(cls, train, disccount):
		if train.number in cls.seat_ticket:
			return [(SEAT, 3.00, None)]
		else:
			return []
