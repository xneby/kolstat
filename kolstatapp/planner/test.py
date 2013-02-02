#!/usr/bin/env python2
# coding: utf-8

import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'kolstat.settings'
sys.path.extend(('../..', '../../..'))

from kolstatapp.models import Station
from make_query import make_simple_query
from datetime import datetime

radom, = Station.search("Radom")
ruda_wielka, = Station.search("Warszawa Wschodnia")
now = datetime(2013, 1, 11, 4, 57)

ans = make_simple_query(radom, ruda_wielka, now)
from pprint import pprint
pprint(ans)
