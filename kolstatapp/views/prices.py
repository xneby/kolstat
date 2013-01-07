from kolstatapp.decorators import expose
from kolstatapp.exceptions import Redirect

from kolstatapp.models import Train, Station, TrainTimetable, TrainStop, Discount
from kolstatapp.utils.cennik import calculate

from django.core.urlresolvers import reverse
from datetime import datetime

@expose('prices/show.html')
def prices_show(request):
	def error():
		raise Redirect(reverse('kolstat-prices-form'))

	if request.method != 'POST' or 'count' not in request.POST:
		error()

	try:
		count = int(request.POST['count'])
	except ValueError:
		error()

	required = ['date', 'count']
	for i in range(count):
		required.extend(['tname' + str(i), 'sfrom' + str(i), 'sto' + str(i)])
	
	for r in required:
		if r not in request.POST:
			error()

	date = datetime.strptime(request.POST['date'], '%d-%m-%Y').date()
	plan = []

	for i in range(count):
		train_name = request.POST['tname' + str(i)]
		station_from = int(request.POST['sfrom' + str(i)])
		station_to = int(request.POST['sto' + str(i)])

		try:
			sfrom = Station.objects.get(pk = station_from)
			sto = Station.objects.get(pk = station_to)
		except Station.DoesNotExist:
			error()

		try:
			train, = Train.search(train_name)
		except Train.DoesNotExist:
			error()

		try:
			tt = train.timetables().get(date = date)
		except TrainTimetable.DoesNotExist:
			error()

		try:
			stop_from = tt.stops().get(station = sfrom)
			stop_to = tt.stops().get(station = sto)
		except TrainStop.DoesNotExist:
			error()

		plan.append((train, stop_from, stop_to))

	outcome = calculate(plan, Discount.objects.all())

	stats = dict()
	operators = dict()
	razem = 0

	for name, oferta, typ, args, znizka, cena in outcome:
		if typ not in stats:
			stats[typ] = 0
		stats[typ] += cena

		if oferta.operator not in operators:
			operators[oferta.operator] = 0
		operators[oferta.operator] += cena

		razem += cena

	return dict(out = outcome, stats = stats, razem = razem, plan = plan, date = date, operators = operators)