#!/usr/bin/env python2
# coding: utf-8

import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'kolstat.settings'
sys.path.extend(('../../../..', '../../../../..'))

from kolstatapp.models import Station
import station

st = Station.objects.all()

s = st[0]

station.query_station(s)
