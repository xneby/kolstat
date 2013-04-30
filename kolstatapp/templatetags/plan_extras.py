# coding: utf-8
from django import template
from kolstatapp.utils.cennik import calculate, calc_price, plan_from_connection

register = template.Library()

@register.simple_tag
def get_price(connection, discounts, typ = "normal"):
	clc = calculate(plan_from_connection(connection), discounts)

	if typ == 'normal':
		return "{:.2f}".format(calc_price(clc))
	elif typ == 'full':
		price = 0.0
		discounts = set()
		classes = set()
		distance = 0.0
		for name, oferta, typ, args, znizka, cena, km in clc:
			if znizka is not None:
				discounts.add(znizka)
			if name == 'base':
				distance += km
			classes.add(oferta.klass)
			price += cena

		description = '{}{}{}'.format('{:.2f}km, '.format(distance),
			('{}, '.format(' oraz '.join('zniżka {} ({}%)'.format(x.description, x.discount) for x in discounts)) if discounts else 'bilet normalny, '),
			'{} klasa'.format(' oraz '.join(x.name for x in classes)))

		return '{:.2f}zł ({})'.format(price, description)
