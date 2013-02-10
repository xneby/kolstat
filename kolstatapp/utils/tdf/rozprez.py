#!/usr/bin/env python2

import os,sys
sys.path.extend(['../../../', '../../../../'])
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.db import connection, transaction
from kolstatapp.models import TrainTimetable
from datetime import date, timedelta

cursor = connection.cursor()

sd = date(2013, 2, 7)
ed = date(2013,12, 7)

dates = []
dzien = timedelta(days = 1)

while sd != ed:
	dates.append(sd)
	sd += dzien

dates.append(ed)

ttids = TrainTimetable.objects.all()

for tid in ttids:
	with transaction.commit_on_success():
		for d in dates:

			tt = TrainTimetable.objects.create(train_id = tid.train_id, date = d)

			cursor.execute('''
					INSERT INTO kolstatapp_trainstop (timetable_id, station_id, arrival, departure, arrival_overnight, departure_overnight, distance, `order`) SELECT %s, station_id, arrival, departure, arrival_overnight, departure_overnight, distance, `order` as ord FROM kolstatapp_trainstop WHERE timetable_id = %s
				''', [tt.id, tid.id])

		print tid

cursor.close()
