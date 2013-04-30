# coding: utf-8

from kolstatapp.models import Discount


class TICKET:
	name = 'Bilet'
	name_plural = 'Bilety'

class SEAT:
	name = 'Miejscówka'
	name_plural = 'Miejscówki'

class DRUGA:
	name = 'druga'

class PIERWSZA:
	name = 'pierwsza'

class Oferta:
	klass = DRUGA
	@classmethod
	def get_additional_prices(cls, train):
		return ()

	@classmethod
	def _get_base_price(cls, distance, discount):

		base_price = 0
		for limit, price in cls.distances:
			if int(round(distance)) <= limit:
				base_price = price
				break
		return [(TICKET, price * (discount.ratio() if discount is not None else 1.0), discount)]

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
		return list(map(Discount.get, d))

	ustawowe = _get_discounts(('DZ/UCZ',))
	IC = _get_discounts(())
	KM = _get_discounts(())
	R = _get_discounts(())
	KW = _get_discounts(())
