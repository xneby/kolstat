#!/usr/bin/env python2
# coding: utf-8

import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'kolstat.settings'
sys.path.extend(('../..', '../../..'))

from kolstatapp.models import Train
from normal_to_hafas import save_cache, acquire, create_connection
from kolstatapp.exceptions import KolstatError
from hafas import HafasObject

import httplib

import threading
import Queue

trains = []

categories = ['EIC']

with open('train_list') as f:
	for l in f:
		if any(l.startswith(x) for x in categories):
			trains.append(l.strip())

with open('non_train') as g:
	for l in g:
		if l.strip() in trains:
			trains.remove(l.strip())

print len(trains)

queue = Queue.Queue()
print_lock = threading.RLock()

class Thread(threading.Thread):
	def __init__(self, queue, print_lock):
		super(Thread, self).__init__()
		self.queue = queue
		self.print_lock = print_lock
		self.hafas = HafasObject()

	def run(self):
		print_lock.acquire()
		print "Thread", self.name
		print_lock.release()
		conn = create_connection()
		while True:
			name = self.queue.get()

			t = None
			while t is None:
				try:
					t = Train.add_train(name, conn, self.hafas)
				except httplib.BadStatusLine:
					conn = create_connection()
				except KolstatError as e:
					print_lock.acquire()
					print name , str(e)				
					print_lock.release()
					break


			if t is not None:
				print_lock.acquire()
				print name, t.get_relation_string()
				print_lock.release()
			self.queue.task_done()

import time

DAEMONS = 5

start = time.time()

def main():
	for tr in trains:
		queue.put(tr)
	for i in range(DAEMONS):
		t = Thread(queue, print_lock)
		t.setDaemon(True)
		t.start()


	queue.join()

main()
print "Elapsed time: {:.3f}s".format(time.time() - start)

