# coding: utf-8
from django import template
from kolstatapp.utils.cennik import calculate, calc_price, plan_from_connection

register = template.Library()

@register.simple_tag
def get_price(connection, discounts):
	return "{:.2f}".format(calc_price(calculate(plan_from_connection(connection), discounts)))
