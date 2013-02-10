# coding: utf-8
from httplib import HTTPConnection
from urllib import urlencode
import re

conn = HTTPConnection('rozklad-pkp.pl')

REG = r'hafasname="([A-Z]* *[0-9]+)"'

def query_station(station):
	params = {
			'input': station.hafasID,
			'selectDate': 'period',
			'dateBegin': '05.02.13',
			'dateEnd': '05.02.13',
			'boardType': 'dep',
			'maxJourneys': '9999',
			'L': 'vs_java3',
			'start': 'Pokaż',
		}

	HEADERS = {
		'Content-Type': 'application/x-www-form-urlencoded',
		}

	pp = urlencode(params)
	print(pp)

	conn.request('POST', '/bin/stboard.exe/pn', pp, HEADERS)
	response = conn.getresponse()
	print response.status, response.reason
	data = response.read()
	if 'Error' in data:
		print data

	ll = re.findall(REG, data)

	return list(re.sub('([A-Z])([0-9])', r'\1 \2', re.sub('  +', ' ', x)) for x in ll)

