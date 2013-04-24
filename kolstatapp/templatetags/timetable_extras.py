# coding: utf-8
from django import template
from django.conf import settings
from kolstatapp.models import Station
from kolstatapp.decorators import reverse
from datetime import date, timedelta
from django.conf import settings

register = template.Library()

MONTH_NAMES = [
	'Styczeń',
	'Luty',
	'Marzec',
	'Kwiecień',
	'Maj',
	'Czerwiec',
	'Lipiec',
	'Sierpień',
	'Wrzesień',
	'Październik',
	'Listopad',
	'Grudzień'
		]

DZIEN = timedelta(1)

@register.simple_tag
def print_month(train, month):
	res = '<table class="ttmonth">'

	res += '<tr><th colspan="7">{}</th></tr>'.format(MONTH_NAMES[month])


	if month >= 0:
		d = date(settings.TIMETABLE_YEAR, month+1, 1)
	else:
		month += 12
		d = date(settings.TIMETABLE_YEAR -1 , month + 1, 1)

	offset = d.weekday()

	if offset:
		res += '<tr>'
		while offset:
			res += '<td />'
			offset -= 1
	
	tts = { x.date for x in train.timetables() }

	while d.month == month +1:
		if d.weekday() == 0:
			res += '<tr>'

		cl = []

		if d == date.today():
			cl.append('today')

		kursuje = d in tts

		if kursuje:
			cl.append('valid')
		elif d <= settings.TIMETABLE_END.date() and d >= settings.TIMETABLE_START.date():
			cl.append('invalid')
		else:
			cl.append('outside')

		if cl:
			cls = ' class="{}"'.format(' '.join(cl))
		else:
			cls = ''

		if train.has_variants():
			url = reverse('kolstat-train-date-variant', args=[train.category.name, train.number, train.variant, d.strftime('%Y-%m-%d')])
		else:
			url = reverse('kolstat-train-date', args=[train.category.name, train.number, d.strftime('%Y-%m-%d')])

		res += '<td{}>{}{}{}</td>'.format(cls,'' if not kursuje else '<a href="{}">'.format(url), d.day, '' if not kursuje else '</a>')

		if d.weekday() == 6:
			res += '</tr>'
			
		d += DZIEN
	
	if d.weekday() != 0:
		while d.weekday() != 0:
			res += '<td />'
			d += DZIEN

		res += '</tr>'

	res += '</table>'
	return res
