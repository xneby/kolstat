from kolstatapp.decorators import expose
from kolstatapp.exceptions import Redirect

from kolstatapp.models import Train, Station, TrainTimetable, TrainStop, Discount
from kolstatapp.utils.cennik import calculate, plan_from_connection

from django.core.urlresolvers import reverse
from datetime import datetime
from kolstatapp.planner.wrapper import Connection

@expose('prices/show.html')
def prices_show(request, connection_id):

	connection = Connection.load(connection_id)

	plan = plan_from_connection(connection)

	outcome = calculate(plan, Discount.objects.all())

	stats = dict()
	operators = dict()
	razem = 0
	odl = 0

	for name, oferta, typ, args, znizka, cena, km in outcome:
		if typ not in stats:
			stats[typ] = (0, 0)
		stats[typ] = tuple(a+b for a,b in zip(stats[typ], (cena, km)))

		if oferta.operator not in operators:
			operators[oferta.operator] = (0, 0)
		operators[oferta.operator] = tuple((a+b) for a,b in zip(operators[oferta.operator],(cena, km)))

		razem += cena
		odl += km


	return dict(out = outcome, stats = stats, razem = razem, plan = plan, date = None, operators = operators, odl = odl)
