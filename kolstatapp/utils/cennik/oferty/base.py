# coding: utf-8

from kolstatapp.models import Discount


class TICKET:
	name = 'Bilet'
	name_plural = 'Bilety'

class SEAT:
	name = 'Miejscówka'
	name_plural = 'Miejscówki'

class Oferta:
	@classmethod
	def get_additional_prices(cls, train):
		return ()

	@classmethod
	def _get_base_price(cls, distance, discount):

		base_price = 0
		for limit, price in cls.distances:
#			print int(round(distance)), limit, price
			if int(round(distance)) <= limit:
				base_price = price
				break
		return [(TICKET, price * discount.ratio(), discount)]

	@classmethod
	def best_discount(cls, discounts):
		valid = (x for x in discounts if x in cls.valid_discounts)
		best = None
		for discount in valid:
			if best is None or discount.discount > best.discount:
				best = discount
		return best


	@classmethod
	def get_base_price(cls, distance, discounts):
		return cls._get_base_price(distance, cls.best_discount(discounts))

	@classmethod
	def get_additional_prices(cls, train, discounts):
		return cls._get_additional_prices(train, cls.best_discount(discounts))

class Discounts:
	def _get_discounts(d):
		return map(Discount.get, d)

	ustawowe = _get_discounts(('DS-J', ))
	IC = _get_discounts(())
	KM = _get_discounts(())
	KW = _get_discounts(())
