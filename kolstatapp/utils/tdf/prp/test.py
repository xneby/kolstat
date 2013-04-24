#!/usr/bin/env python2
# coding: utf-8

import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'kolstat.settings'
sys.path.extend(('../../../..', '../../../../..'))

from kolstatapp.models import Station
import train

import sqlite3

conn = sqlite3.connect('db.db')
c = conn.cursor()

c.execute('SELECT count(*) FROM trains')
for wsz, in c: pass

c.execute('SELECT count(*) FROM trains WHERE done = 2')
for zrob, in c: pass

import threading

dbLock = threading.Lock()
printLock = threading.Lock()

class Watek(threading.Thread):
	def run(self):
		global zrob

		self.conn = train.get_connection()
		self.db = sqlite3.connect('db.db')
		self.c = self.db.cursor()

		while True:
			dbLock.acquire()
			self.c.execute('SELECT name FROM trains WHERE done = 0 LIMIT 1')
			num = None
			for num, in self.c: pass
			if num is None:
				dbLock.release()
				break
			self.c.execute('UPDATE trains SET done = 1 WHERE name = ?', [num])
			self.db.commit()
			dbLock.release()

			printLock.acquire()
			zrob += 1
			print('{} -- {}/{} - {}'.format(self.getName(), zrob , wsz, num))
			printLock.release()

			train.query_train(num, self.conn)

			dbLock.acquire()
			self.c.execute('UPDATE trains SET done = 2 WHERE name = ?', [num])
			self.db.commit()
			dbLock.release()

for i in range(5):
	w = Watek()
	w.start()

