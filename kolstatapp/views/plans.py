from kolstatapp.decorators import expose, login_required
from kolstatapp.exceptions import Redirect
from kolstatapp.forms import SimpleQueryForm
from kolstatapp.models import Station
from kolstatapp.planner import wrapper

from django.core.urlresolvers import reverse

from datetime import datetime

@login_required
@expose('plans/list.html')
def plans_list(request):
	return dict()

@expose('plans/new.html')
def plans_new(request):
	if request.method == 'POST':
		form = SimpleQueryForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			
			st_start = data['start']
			st_end = data['end']
			when = datetime.combine(data['date'], data['time'])

			raise Redirect(reverse('kolstat-plans-query', args = [st_start.slug, st_end.slug, when.strftime('%Y-%m-%dT%H:%M:%S')]))

	else:
		form = SimpleQueryForm()

	return dict(form = form)

@expose('plans/query.html')
def plans_query(request, st_start, st_end, when):
	
	try:
		when = datetime.strptime(when, '%Y-%m-%dT%H:%M:%S')
		st_start, = Station.search(st_start)
		st_end, = Station.search(st_end)
	except ValueError:
		raise
		raise Redirect(reverse('kolstat-plans-new'))

	connections = wrapper.make_query(st_start, st_end, when)

	return dict(conn = connections, source = st_start, destination = st_end, when = when)

