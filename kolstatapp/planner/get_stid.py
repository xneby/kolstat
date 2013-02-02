#!/usr/bin/env python2
# coding: utf-8

import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'kolstat.settings'
sys.path.extend(('../..', '../../..'))

from kolstatapp.models import Station
from make_query import make_simple_query
from datetime import datetime

for x in sys.argv[1:]:
		
	try:
		if x.isdigit():
			radom, = Station.objects.filter(pk = int(x))
		else:
			radom, = Station.search(x)
	except ValueError:
		print "NOPE"
	else:
		print radom.pk, radom.name
