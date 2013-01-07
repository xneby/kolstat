# coding: utf-8
import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'kolstat.settings'
sys.path.extend(('../../../', '../../../../'))

from kolstatapp.models import Train, Discount, TrainStop, Station
from datetime import date

discounts = Discount.objects.all()

KM6014, = Train.search('KM 6014')
TLK31108, = Train.search('TLK 31108')
TLK15117, = Train.search('TLK 15117')

RW, = Station.search('Ruda Wielka')
RA, = Station.search('Radom')
WW, = Station.search('Warszawa Wschodnia')
GD, = Station.search('Gdynia Główna')

dzien = date(2013, 1, 3)

Ruda_Wielka = TrainStop.objects.get(timetable__date = dzien, timetable__train = KM6014, station = RW)
Radom1 = TrainStop.objects.get(timetable__date = dzien, timetable__train = KM6014, station = RA)

Radom2 = TrainStop.objects.get(timetable__date = dzien, timetable__train = TLK31108, station = RA)
WW1 = TrainStop.objects.get(timetable__date = dzien, timetable__train = TLK31108, station = WW)

WW2 = TrainStop.objects.get(timetable__date = dzien, timetable__train = TLK15117, station = WW)
Gdynia = TrainStop.objects.get(timetable__date = dzien, timetable__train = TLK15117, station = GD)

plan = [
	(KM6014, Ruda_Wielka, Radom1),
	(TLK31108, Radom2, WW1),
	(TLK15117, WW2, Gdynia)
]

import pprint
pprint.pprint(plan)

from calculator import calculate

cena = calculate(plan, discounts)

pprint.pprint(cena)
