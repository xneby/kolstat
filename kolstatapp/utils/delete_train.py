#!/usr/bin/env python2
# coding: utf-8

import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'kolstat.settings'
sys.path.extend(('../..', '../../..'))

from kolstatapp.models import Train
from .normal_to_hafas import save_cache, acquire

x = input('Podaj pociąg (np. KM 6010) ').strip()

if ' ' in x:
	oper, numer = x.split(' ')
else:
	oper = ''
	numer = x

tt = Train.search(x)

if len(tt) > 0:
	t, = tt
	t.delete_train()
else:
	print("Brak pociągu")
