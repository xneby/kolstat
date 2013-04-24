# coding: utf-8
from kolstatapp.decorators import expose, Redirect, reverse
from kolstatapp.utils.hafas import HafasTrain
from kolstatapp.models import Train, TrainTimetable

from kolstatapp.exceptions import KolstatError

import datetime 
@expose('train.html')
def train(request, operator, number, variant = None):
	res = Train.search(operator + ' ' + number, variant)
	if len(res) != 1:
		raise Redirect(reverse('kolstat-trains-search'))

	ktrain, = res

	return dict(train = ktrain)

@expose('train-date.html')
def train_date(request, operator, number, variant = None, date = None):
	res = Train.search(operator + ' ' + number, variant)
	if len(res) != 1:
		raise Redirect(reverse('kolstat-trains-search'))

	ktrain, = res
	
	d = datetime.datetime.strptime(date, '%Y-%m-%d').date()

	try:
		tt, = ktrain.traintimetable_set.filter(date = d).select_related()
	except ValueError:
		raise KolstatError('Pociąg nie kursuje w tym dniu')

	table = {}
	stations = []

	trains = [tt] + tt.get_coupled()

	juz = 0

	for t in trains:
		ans = []
		for s in t.stops():
			ans.append((s.station, s))

		not_added=[]

		last = -1

		for st, s in ans:
			if st in list(table.keys()):
				while len(table[st]) != juz:
					table[st].append("")
				table[st].append(s)
				idx = stations.index(st)
				stations[idx:idx] = not_added
				last = idx + len(not_added)
				not_added = []
			else:
				table[st] = [""] * juz + [s]

				not_added.append(st)

		stations[last+1:last+1] = not_added
		not_added = []
		juz += 1

	pres = []

	print(stations)
	print(table)

	for st in stations:
		while len(table[st]) < juz:
			table[st].append("")
		km = []
		stops = []
		short = False

		pocz = True
		kon = True
		
		for s in table[st]:
			if type(s) == type(""):
				km.append("")
				stops.append(None)
			else:
				km.append(s.distance)
				stops.append(s)
				short |= s.is_short()
				if s.arrival is not None:
					pocz = False
				if s.departure is not None:
					kon = False

		pres.append((km, st, short, pocz, kon, stops))

	import pprint
	pprint.pprint(pres)

	return dict(train = ktrain, timetable = tt, table = pres, ile = juz, trains = [x.train for x in trains])
