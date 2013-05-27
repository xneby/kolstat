# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from kolstatapp.utils.traincat import get_img_url, get_operator, get_category_class, get_full_name, get_category, get_all
from kolstatapp.models import Train, TrainTimetable

register = template.Library()

@register.simple_tag
def traincat_img_url(train):
	return get_img_url(train)

@register.simple_tag
def train_operator(train):
	return get_operator(train)

@register.simple_tag
def train_category_class(train):
	return get_category_class(train)

@register.simple_tag
def train_category(train):
	return get_category(train)

@register.simple_tag
def train_name(train):
	return ''

@register.simple_tag
def train_category_explanation(train):
	return get_full_name(train)

@register.simple_tag
def print_composition(comp):
	cars = comp.split('+')
	return "".join('<img src="/static/img/carriages/{name}.png" alt="{name}" />'.format(name = x) for x in cars)

class TraincatGetNode(template.Node):
	def __init__(self, varname):
		self.varname = varname

	def render(self, context):
		context[self.varname] = get_all()
		return ''

@register.tag
def traincat_get(parser, token):
	args = token.contents.split()

	return TraincatGetNode(args[2])

@register.simple_tag
def train_overview(train):
	t = template.loader.get_template('trains/_train_overview.html')
	return t.render(template.Context(dict(train = train)))

@register.simple_tag
def train(train, date = None):
	link = None
	if isinstance(train, Train):
		link = train.get_absolute_url(date)
		name = "{} {}".format(train.category.name, train.number)
	elif isinstance(train, TrainTimetable):
		link = train.train.get_absolute_url(train.date)
		name = "{} {}".format(train.train.category.name, train.train.number)
	else:
		name = "###ARG!"

	if link is not None:
		result = '<a href="{link}">{name}</a>'.format(link = link, name = name)
	else:
		result = name

	return '<span class="train">{}</span>'.format(result)

