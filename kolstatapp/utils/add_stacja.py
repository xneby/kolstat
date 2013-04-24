#!/usr/bin/env python2
# coding: utf-8

import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'kolstat.settings'
sys.path.extend(('../..', '../../..'))

from kolstatapp.models import Station
from .normal_to_hafas import Hafas

nazwa = input('Podaj nazwę stacji: ')
hs = Hafas.searchStation(nazwa)[0]
print(hs.toString())
gsk = int(input('gsk: '))
try:
	s, = Station.search(hs.externalId)
except ValueError:
	s = Station()

s.gskID = gsk
s.hafasID = hs.externalId
s.name = hs.name
print(s)
s.save()
