#!/usr/bin/env python2
# coding: utf-8

import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'kolstat.settings'
sys.path.extend(('../..', '../../..'))

from kolstatapp.models import Train
from normal_to_hafas import save_cache, acquire

x = raw_input('Podaj pociąg (np. KM 6010) ').strip()

tt = Train.search(x)

if len(tt) > 0:
	t, = tt
	print "Było"
else:
	t = Train.add_train(x)

print t.get_relation_string()
