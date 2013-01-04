#!/usr/bin/env python2
# coding: utf-8

import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'kolstat.settings'
sys.path.extend(('../..', '../../..'))

from kolstatapp.models import Station
from normal_to_hafas import Hafas

nazwa = raw_input('Podaj nazwę stacji: ')
hs = Hafas.searchStation(nazwa)[0]
print hs.toString()

s = Station(name = hs.name, hafasID = hs.externalId, gskID = int(raw_input('gsk: ')))
print s
s.save()
