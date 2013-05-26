# -*- coding: utf-8 -*-
from django.conf import settings
from kolstatapp.models import TrainCategory

ORDER = ('EIC', 'EX', 'TLK', 'EC', 'EN', 'D', 'RE', 'IR', 'R', 'AR', 'KD', 'KM', 'KW', 'KS', 'SKM', 'SKW', 'WKD')

def get_all():
	return [TrainCategory.objects.get(name = x) for x in ORDER]

def get_img_url(train):
	return train.category.url()

def get_full_name(train):
	return train.category.full_name

def get_operator(train):
	return train.category.operator.name

def get_category_class(train):
	return train.category.get_type_class()

def get_category(train):
	return train.category.name
