#!/usr/bin/env python2
# coding: utf-8

import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'kolstat.settings'
sys.path.extend(('../../../', '../../../../'))

from kolstatapp.models import Train
from library import import_from_file
import Queue
import threading

files = sys.argv[1:]

queue = Queue.Queue()
for i in files:
	queue.put(i)

stdout = threading.Lock()
done = 0

class Watek(threading.Thread):
	def run(self):
		while not queue.empty():
			try:
				name = queue.get(False)
			except Queue.Empty:
				break

			with stdout:
				global done
				print self.getName(), name, done, queue.qsize()
				done += 1

			with open(name) as f:
				import_from_file(f)

for i in range(5):
	w = Watek()
	w.start()

