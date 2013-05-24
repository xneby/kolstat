#!/usr/bin/env python3
# coding: utf-8

import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'kolstat.settings'
sys.path.extend(('../..', '../../..'))

from kolstatapp.models import Station
from normal_to_hafas import Hafas

nazwa = input('Podaj nazwę stacji: ')
hs = Hafas.searchStation(nazwa)[0]
print(hs.toString())
try:
	s, = Station.search(hs.externalId)
	print(s.id)
	sys.exit(0)
except ValueError:
	s = Station()

gsk = int(input('gsk: '))
s.gskID = gsk
s.hafasID = hs.externalId
s.name = hs.name
print(s)
s.save()
print(s.id)
