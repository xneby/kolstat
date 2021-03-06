#!/usr/bin/env python3
# coding: utf-8

import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'kolstat.settings'
sys.path.extend(('../../../', '../../../../'))

from kolstatapp.models import Train
from library import import_from_file
import queue
import threading

files = sys.argv[1:]

queue = queue.Queue()
for i in files:
	queue.put(i)

dijkstra_lock = threading.Lock()
mysql_lock = threading.Lock()
stdout = threading.Lock()
done = 0

class Watek(threading.Thread):
	def run(self):
		while not queue.empty():
			try:
				name = queue.get(False)
			except queue.Empty:
				break

			with stdout:
				global done
				print(self.getName(), name, done, queue.qsize())
				done += 1

			with open(name) as f:
				import_from_file(f, dijkstra_lock, mysql_lock)

for i in range(5):
	w = Watek()
	w.start()

