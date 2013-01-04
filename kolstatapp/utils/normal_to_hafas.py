#!/usr/bin/env python2
# coding: utf-8

import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'kolstat.settings'
sys.path.extend(('../..', '../../..'))

#from kolstatapp.models import Station
from hafas import Hafas, HafasTrain
from datetime import date, timedelta
from kolstatapp.models import Station
from kolstatapp.exceptions import DeprecationError

import httplib
import urllib
import re
import operator
from xml.dom import minidom

from django.conf import settings
import cache

SERVER = 'rozklad-pkp.pl'


REGEXP = r'<tr class="zebracol-[0-9]">\s*<td class="nowrap">\s*<a href="http://{server}/bin/traininfo.exe/pn/(\d+/\d+/\d+/\d+/51)\?trainname=(?:[^&]*)&amp;backLink=ts&amp;"><img src="(?:[^"]+)" width="28" height="30" alt="(?:[^"]+)" style="margin-right:3px;">&nbsp;([^<]+)</a>\s*</td>\s*<td class="nowrap">([^<]+)</td>*\s+<td class="nowrap">([^<]+)</td>*\s+<td>\s*<a href="http://rozklad-pkp.pl/bin/traininfo.exe/pn/\1\?"><img src="/hafas-res/img/traininfo.gif" width="23" height="23" alt=""></a>\s*</td>\s*<td>\s*([^<]+)</td>\s*</tr>'

ENTITIES = {
'&#380;': 'ż',
'&#243;': 'ó',
'&#322;': 'ł',
'&#378;': 'ź',
'&#281;': 'ę',
'&#346;': 'Ś',
'&#324;': 'ń',
'&#347;': 'ś',
		}

MONTHS = {
	'Sty': 1,
	'Lut': 2,
	'Mar': 3,
	'Kwi': 4,
	'Maj': 5,
	'Cze': 6,
	'Lip': 7,
	'Sie': 8,
	'Wrz': 9,
	'Paź': 10,
	'Pa\xc5': 10,
	'Lis': 11,
	'Gru': 12
		}

DTYG = {
	'Pn': 0,
	'Wt': 1,
	'Śr': 2,
	'Cz': 3,
	'Pt': 4,
	'So': 5,
	'Nd': 6,
}

YEAR = settings.TIMETABLE_YEAR

def polskie(name):
	try:
		Station.objects.get(name = name)
		return True
	except Station.DoesNotExist:
		return False

def normalize(x):
	for k, v in ENTITIES.items():
		x = x.replace(k,v)
	return x

dzien = timedelta(1)

def przedzial(a, b, f = None):
	s = set()

	s.add(b)

	while a not in s:
		if f is None or a.weekday() in f:
			s.add(a)
		a += dzien

	return s

def calosc():
	return przedzial(settings.TIMETABLE_START, settings.TIMETABLE_END)

WSZYSTKO = calosc()

def parse_dni(s):

	tokens = s.replace(';', '').replace(',', '').split()
	tokens += ['']

	state = 'kursuje'

	def is_day(token):
		return re.match(r'\d+\.', token) is not None

	def is_month(token):
		return token in MONTHS

	def is_year(token):
		return re.match(r'20\d{2}', token) is not None

	def is_filter(token):
		return token in DTYG or token == '-'

	wdo = None
	la = None
	prz = False

	wm = []
	wy = []
	dni = set()

	wynik = set()

	def fin(la):
		if la is None: return
		if len(la) == 1:
			wm.append(la[0])
		if len(la) == 2:
			wy.append(la)
		if len(la) == 3:
			dni.add(date(*reversed(la)))

	def przedz(wdo, _la):
		if len(wdo) == 1:
			wm.extend(list(range(wdo[0], _la[0]+1)))
		elif len(wdo) == 2:
			while wdo != _la:
				wy.append(wdo)
				twdo = date(settings.TIMETABLE_YEAR, wdo[1], wdo[0]) + dzien
				wdo = [twdo.day, twdo.month]
			wy.append(_la)
		elif len(wdo) == 3:
			while wdo != _la:
				dni.add(date(*reversed(wdo)))
				twdo = date(wdo[2], wdo[1], wdo[0]) + dzien
				wdo = [twdo.day, twdo.month, twdo.year]
			dni.add(date(*reversed(_la)))
		la = None

	flts = []

	for token in tokens:

		if is_filter(token):
			flts.append(token)
		elif len(flts) > 0:

			if len(dni) == 0:
				dni = calosc()

			wd = []

			for t in range(len(flts)):
				try:
					if flts[t] == '-':
						wd.extend(range(DTYG[flts[t-1]], DTYG[flts[t+1]]+1))
					else:
						wd.append(DTYG[flts[t]])
				except IndexError:
					print flts, t
					raise

			flts = []
			if wd == []:
				wd = range(7)

			if state == 'kursuje':
				wynik -= dni

			dni = set(filter(lambda x: x.weekday() in wd, dni))

			la = None

			if state == 'kursuje':
				wynik |= dni
			else:
				wynik -= dni
			dni = set()

		if token == 'codziennie':
			wynik |= calosc()

		if token == 'do':
			prz = True
			wdo = la
			la = None

		if is_day(token):

			fin(la)

			la = [int(token[:-1])]
			
			if prz and len(la) > 1:
				wrzuc_prz()
				prz = False
				wdo = None

		if is_month(token):

			if len(la) == 1:
				la.append(MONTHS[token])
			else:
				fin(la)
				la = None

			if prz and len(wdo) == 1:
				przedz(wdo, la)
				prz = False

			wy.extend([x, MONTHS[token]] for x in wm)
			wm = []

		if is_year(token):
			if not prz:
				la.append(int(token))
			if prz and len(wdo) == 2:
				przedz(wdo, la)
				prz = False
			elif prz and len(wdo) == 3:
				la.append(int(token))
				przedz(wdo, la)
				prz = False

			for x in wy:
				dni.add(date(int(token), x[1], x[0]))
				wy = []

		if token in ('oprócz', 'także'):
			for x in wy:
				x = date(settings.TIMETABLE_YEAR, x[1], x[0])
				if x not in WSZYSTKO:
					x = date(x.year - 1, x.month, x.day)

				dni.add(x)

			fin(la)
			la = None
			if state == 'kursuje':
				wynik |= dni
			else:
				wynik -= dni

			dni = set()

			if state == 'kursuje':
				state = 'oprocz'
			else:
				state = 'kursuje'


	
#	print wm, wy, la
	
	fin(la)
	for x in wy:
		x = date(settings.TIMETABLE_YEAR, x[1], x[0])
		if x not in WSZYSTKO:
			x = date(x.year - 1, x.month, x.day)

		dni.add(x)

	
	if state == 'kursuje':
		wynik |= dni
	else:
		wynik -= dni

	return wynik

def create_connection():
	return httplib.HTTPConnection(SERVER)

def the_same(a,b):
	return a.replace(' ', '') == b.replace(' ', '')

def acquire(name, conn = None):
	if name.startswith('R '):
		name = name[2:]
	if conn is None:
		conn = httplib.HTTPConnection(SERVER)
	conn.request('GET', '/bin/trainsearch.exe/pn?trainname={}'.format(urllib.quote(name)))
	resp = conn.getresponse()

	data = resp.read()

	res = re.findall(REGEXP.format(server = SERVER), data, re.DOTALL | re.MULTILINE)

	variants_rel = {}
	variants = {}
	variants_no = 0

	for dkod, nr, skad, dokad, dnikursowania in res:
		if not the_same(nr.strip(), name):
			continue

		skad = normalize(skad)
		dokad = normalize(dokad)

		if not polskie(skad) or not polskie(dokad):
			continue

		dnikursowania = normalize(dnikursowania).strip()
		
		vrel = skad, dokad

		variant = None

		for k, v in variants_rel.items():
			if skad in k or dokad in k:
				nk = list(k)
				if skad not in k:
					nk.append(skad)
				if dokad not in k:
					nk.append(dokad)

				nk = tuple(nk)

				del variants_rel[k]
				variants_rel[nk] = v
				variant = v
				

		if variant is None:
			variants_no += 1
			variant = chr(variants_no + 64)
			variants[variant] = ({}, {}, [], [], 1)
			variants_rel[vrel] = variant

		result, roz, ss, dd, rk = variants[variant]
		
		_, wazne = dnikursowania.split('kursuje:')
		pd = parse_dni(wazne.strip())

		arr = Station.search(dokad)[0].hafasID
		dep = Station.search(skad)[0].hafasID
		
		url = '/bin/traininfo.exe/pn/{}?L=vs_java3'.format(dkod)
		conn.request('GET', url)
		resp = conn.getresponse()
		data = resp.read()
		
		dom = minidom.parseString('<main>{}</main>'.format(data))
		main,  = dom.childNodes
		elems = main.getElementsByTagName('St')
		first = elems[0]
		
		deptime = first.getAttribute('depTime')
		
		if dep not in ss:
			ss.append(dep)

		if arr not in dd:
			dd.append(arr)

		for day in pd:
			tt = "1{:0>9}{:0>9}{}{}".format(dep,arr,day.strftime('%Y%m%d'),deptime.replace(':',''))
			tt = "{:x}".format( int(tt))
			result[day] = tt
			roz[day] = rk

		rk += 1

		variants[variant] = (result, roz, ss, dd, rk)

	return {v: dict(source = ss, destination = dd, ids = result, roz = roz) for v, (result, roz, ss, dd, _) in variants.items() }

def get_relation(number):
	raise DeprecationError()
	res = acquire(number)
	
	return res['source'], res['destination']

def getId(number, day = None):
	raise DeprecationError()
	ids = acquire(number)['ids']
	if day is not None:
		return ids[day]
	return ids

def save_cache(number, variant, _ = None, hafas = None):
	if _ is None:
		_ = acquire(number)
	result = _['ids']
	roz = _['roz']

	h = {}

	for day in result:
		if roz[day] in h:
			cache.link(result[day], h[roz[day]])
		else:
			_, conn = HafasTrain.connFromId(result[day], hafas)
			h[roz[day]] = result[day]
			cache.save(conn, result[day])


if __name__ == '__main__':
	import pprint
	x = acquire(raw_input('Podaj numer'))
#	print parse_dni('12. Gru 2011 do 30. Mar 2012 Pn - Pt; 27. Lip do 7. Gru 2012 Pn - Pt; oprócz 26. Gru, 6. Sty, 15. Sie, 1. Lis')
#	x = parse_dni("1. do 28. Cze 2012 Pn - Pt; oprócz 7. Cze")
	pprint.pprint(x)
