#!/usr/bin/env python2
# coding: utf-8

import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'kolstat.settings'
sys.path.extend(('../../..', '../../../..'))

from graph import Graph

g = Graph()
with open('graph.out', 'w') as f:
	g.save_to(f)

