# coding: utf-8
from http.client import HTTPConnection
from urllib.parse import urlencode
import re
import html.parser
from pprint import pprint
import operator
import urllib.parse
from from_html import parse
from datetime import date

import os, sys
from functools import reduce

sys.path.extend(['../../../../'])
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from kolstat.kolstatapp.models import Station

def get_connection():
	return HTTPConnection('rozklad.sitkol.pl')

REG = '''
<a href="([^"]*)"[^>]*><img src="/hafas-res/img/(?:[a-z]*)_pic.gif" width="28" height="30" alt="([^"]*)" style="margin-right:3px;">\xa0[^<]*</a>
</td>
<td class="nowrap">([^<]*)</td>
<td class="nowrap">([^<]*)</td>'''

def polskie(names):
	ll = Station.objects.filter(name__in = names).values_list('name')
	ll = reduce(operator.add, ll, ())

	mm = dict()

	for n in names:
		if n in ll:
			mm[n] = True
		else:
			mm[n] = False
	
	return mm

def query_train(train, conn):
	params = {
		'date': '05.02.13',
		'trainname': train,
	}

	HEADERS = {
		'Content-Type': 'application/x-www-form-urlencoded',
		}

	pp = urlencode(params)
#	print(pp)

	conn.request('POST', '/bin/trainsearch.exe/pn', pp, HEADERS)
	response = conn.getresponse()
#	print response.status, response.reason
	data = response.read()
#	print 'read'
	data = html.parser.HTMLParser().unescape(data)
#	print 'parsed'
	np = re.findall(REG, data, re.DOTALL)
	ll = []
	st = []
	for _,_,y,z in np:
		st.extend((y,z))

	mm = polskie(st)

	for x,p,y,z in np:
		if (mm[y] and mm[z]) and re.sub(' +', '', p) == re.sub(' +', '', train):
			ll.append((x,p,y,z))

	if len(ll) == 0 and train.startswith('TLK'):
		query_train(re.sub('TLK','D',train), conn)
		return 

	for i, (x,nr,_,_) in enumerate(ll):
		var = chr(65 + i)

		t = urllib.parse.urlparse(x)

		nr = re.sub(' +', '', nr)
		if nr.isdigit():
			nr = 'R' + nr

		conn.request('GET', t.path)
		response = conn.getresponse()
#		print response.status, response.reason
		data = response.read()
		data = html.parser.HTMLParser().unescape(data)
		xx = parse(data, nr, date(2013, 2, 5), var) 

		with open('trains/{}{}.yaml'.format(nr,var), 'w') as f:
			f.write(xx)
