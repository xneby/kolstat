#!/usr/bin/env python3
# coding: utf-8

import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'kolstat.settings'
sys.path.extend(('../../..', '../../../..'))

from graph import Graph

g = Graph()
with open('graph.out', 'wb') as f:
	g.save_to(f)

