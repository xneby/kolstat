from kolstatapp.decorators import expose
from kolstatapp.exceptions import KolstatError, Redirect
from kolstatapp.models import Station, TrainName, Train, Journey
from kolstatapp.utils.hafas import Hafas, HafasTrain
from kolstatapp.utils.traincat import get_img_url
from kolstatapp.utils.composition import parse_composition

from datetime import datetime, timedelta

from django.core.urlresolvers import reverse

@expose('journeys/add.html')
def journey_add(request):
	if request.method == 'POST':
		required = ('start', 'end', 'date')
		for field in required:
			if field not in request.POST:
				raise KolstatError('Incomplete request')

		nVia = 0
		while 'via{}'.format(nVia+1) in request.POST:
			nVia += 1

		stations = []

		for x in [request.POST['start']] + [request.POST['via{}'.format(x)] for x in range(1,nVia+1)] + [request.POST['end']]:
			res = Station.search(x)
			if len(res) == 1:
				stations.append(res[0])
			else:
				raise KolstatError('Multiple stations returned')

		request.session['date'] = datetime.strptime(request.POST['date'], '%d-%m-%Y')
		request.session['stations'] = [st.pk for st in stations]
		request.session['step'] = 1

		raise Redirect(reverse('journey-add-step2'))

	return dict()

@expose('journeys/add-step2.html')
def journey_add_step2(request):

	if 'stations' not in request.session or 'date' not in request.session or 'step' not in request.session:
		raise Redirect(reverse('journey-add'))

	stations = request.session['stations']
	stations = [Station.objects.get(pk = st) for st in stations]
	date = request.session['date']
	step = request.session['step']

	if step == len(stations):
		raise Redirect(reverse('journey-add-end'))
	else:
		start = stations[step - 1]
		end = stations[step]

		print start, end, date

		trains = Train.get_trains(start, end, date)

		return dict(start = start, end = end, trains = trains, date = date)

@expose('journeys/add-step3.html')
def journey_add_step3(request):
	if request.method != 'POST':
		raise Redirect(reverse('journey-add'))

	if 'stations' not in request.session or 'date' not in request.session or 'step' not in request.session:
		raise Redirect(reverse('journey-add'))

	stations = request.session['stations']
	stations = [Station.objects.get(pk = st) for st in stations]
	date = request.session['date']
	step = request.session['step']

	if 'tid' not in request.POST:
		raise Redirect(reverse('journey-add'))

	tid = request.POST['tid']

	request.session['tid'] = tid

	train = HafasTrain.fromId(tid)

	ktrain = Train.fromHafas(train)

	return dict(train = train, compositions = ktrain.get_compositions()[:5])

@expose('')
def journey_add_finitialize(request):
	
	def parse(x):
		y = request.POST[x]
		try:
			y = int(y)
		except ValueError:
			raise KolstatError('Bad request')
	
		if 0 <= y <= 5:
			return y
		else:
			raise KolstatError('Bad request')
	
	if request.method != 'POST':
		raise Redirect(reverse('journey-add'))
	
	if 'stations' not in request.session or 'date' not in request.session or 'step' not in request.session or 'tid' not in request.session:
		raise Redirect(reverse('journey-add'))
	
	if 'delay' not in request.POST or 'composition' not in request.POST or 'clean' not in request.POST:
		raise KolstatError('Incomplete request')
	
	delay = parse('delay')
	clean = parse('clean')
	tid = request.session['tid']
	
	composition = parse_composition(request.POST['composition'])
	
	hafas_train, connection = HafasTrain.connFromId(tid)
	train = Train.fromHafas(hafas_train)
	
	def _(x):
		return Station.objects.get(hafasID = x)

	j = Journey()
	j.source = _(hafas_train.source.externalId)
	j.destination = _(hafas_train.destination.externalId)
	j.trainId = tid
	j.date = hafas_train.date

	if request.user.is_authenticated():
		j.user = request.user
	j.delay_vote, j.clean_vote, j.composition_vote = train.add_vote(delay, clean, composition)
	
	j.save()

	request.session['step'] += 1
	request.session['date'] = datetime.combine(request.session['date'].date, connection.arrival.time)
	
	raise Redirect(reverse('journey-add-step2'))

@expose('journeys/add_end.html')
def journey_add_end(request):
	return dict()
