from httplib import HTTPConnection
from urllib import urlencode

conn = HTTPConnection('rozklad.sitkol.pl')

def query_station(station):
	params = {
			'input': 'Radom', #station.hafasID,
			'selectDate': 'today',
#			'dateBegin': '04.02.13',
#			'dateEnd': '04.02.13',
			'boardType': 'dep',
			'maxJourneys': 99,
#			'time': '00:00',
#			'timeSlots': '1',
			'L': 'vs_java3',
		}

	HEADERS = {
		'Content-Type': 'application/x-www-form-urlencoded',
			}

	conn.request('POST', '/bin/stboard.exe/dn?ld=c', urlencode(params), HEADERS)
	response = conn.getresponse()
	print response.status, response.reason
	data = response.read()
	print data
	print urlencode(params)


