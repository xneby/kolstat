#!/usr/bin/env python2
# coding: utf-8

import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'kolstat.settings'
sys.path.extend(('../../../', '../../../../'))

from kolstatapp.models import Train
from library import import_from_file

for name in sys.argv[1:]:
	print name
	with open(name) as f:
		import_from_file(f)
