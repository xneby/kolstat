from kolstatapp.decorators import expose, login_required
from kolstatapp.exceptions import Redirect
from kolstatapp.forms import SimpleQueryForm
from kolstatapp.models import Station
from kolstatapp.planner import wrapper

from django.core.urlresolvers import reverse
from django.template import Template, RequestContext
from django.template.loader import get_template
from django.http import HttpResponse

from subprocess import Popen, PIPE
from datetime import datetime
import shlex
import qrcode
import base64
import io
import json

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

def get_plan_json(request, connection_id):

	conn = wrapper.Connection.load(connection_id)

	answer = dict()
	answer['cid'] = connection_id
	answer['source'] = conn.source.to_json()
	answer['destination'] = conn.destination.to_json()
	answer['arrival'] = conn.arrival
	answer['departure'] = conn.departure

	sections = []
	for s in conn.sections:
		sec = dict()
		sec['source'] = s.source.to_json()
		sec['destination'] = s.destination.to_json()
		sec['arrival'] = s.arrival
		sec['departure'] = s.departure
		sec['train'] = s.train.to_json()
		sec['stops'] = list(x.to_json() for x in s.stops)
		sections.append(sec)
	answer['sections'] = sections

	dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None
	return HttpResponse(json.dumps(answer, default = dthandler), mimetype='application/json')

#@expose('plans/reiseplan.html')
def reiseplan(request, connection_id):

	conn = wrapper.Connection.load(connection_id)
	
	x = io.BytesIO()
	image = qrcode.QRCode(border=0)
	image.add_data(connection_id)
	image.make()
	image.make_image().save(x)
	qr = base64.b64encode(x.getbuffer().tobytes())

	t = get_template('plans/reiseplan.html')
	c = RequestContext(request, dict(connection = conn, qrcode = qr))
	d = bytes(t.render(c), 'utf8')

	if 'raw' not in request.GET:
		pdf = Popen(shlex.split('wkhtmltopdf - -'), stdin = PIPE, stdout = PIPE).communicate(d)[0]

		response = HttpResponse(pdf)
		response['Content-type'] = 'application/pdf';
	else:
		response = HttpResponse(d)

	return response
