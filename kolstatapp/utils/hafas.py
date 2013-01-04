#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import httplib, urllib
from xml.dom.minidom import parseString
from datetime import timedelta, time, datetime, date
from gsk.dijkstra import Dijkstra

import cache

Station = None

def getText(element):
	return element.firstChild.toxml().strip()

class HafasException(Exception):
	def __init__(self, code, text):
		super(HafasException, self).__init__(u'[{}]: {}'.format(code, text))

class HafasError(HafasException): pass
class HafasWarning(HafasException): pass

class HafasStation(object):
	"""klasa przechowująca dane stacji"""
	def __init__(self, name, externalId, cords):
		self.name = name
		self.externalId = externalId
		self.cords = cords

	def __unicode__(self):
		return self.toString()

	def __str__(self):
		return self.name

	def toString(self):
		return u"<Station {obj.name}; id={obj.externalId}; cords={obj.cords}>".format(obj = self)

	def toHafasString(self):
		return u'<Station externalId="{}" />'.format(self.externalId)

	def __repr__(self):
		return self.toString()

	def gskID(self):
		global Station
		if Station is None:
			from kolstatapp.models import Station as x
			Station = x

		s,= Station.search(self.externalId)
		return s.gskID

	@staticmethod
	def fromDOMElement(element, nr = 'externalStationNr'):
		name = element.getAttribute('name')
		id = element.getAttribute(nr)
		x = int(element.getAttribute('x'))
		y = int(element.getAttribute('y'))
		
		return HafasStation(name, id, [x, y])

	def __eq__(self, other):
		if type(other) != type(self):
			return False
		return int(self.externalId) == int(other.externalId)

class HafasConnectionList(object):
	"""klasa przechowująca listę połączeń"""
	def __init__(self, context):
		self.list = []
		self.context = context

	def prev(self):
		raise NotImplementedError

	def next(self):
		connectionList = Hafas.getMoreConnections(self.context, 6)
		self.context = connectionList.context
		self.list.extend(connectionList[:])

	def append(self, connection):
		self.list.append(connection)

	def __getitem__(self, id):
		return self.list[id]

	def __iter__(self):
		return iter(self.list)

	def pop(self, x = None):
		if x is not None:
			self.list.pop(x)
		else:
			self.list.pop()

	def __len__(self):
		return len(self.list)

	def remove(self, id):
		return self.list.remove(id)

	@staticmethod
	def fromDOMElement(dom):
		element, = dom.getElementsByTagName('ConRes')
		context = dom.getElementsByTagName('ConResCtxt')[0].firstChild.toxml().strip()
		connectionList = HafasConnectionList(context)
		for connectionDOM in element.getElementsByTagName('Connection'):
			connectionList.append(HafasConnection.fromDOMElement(connectionDOM))

		return connectionList

class HafasConnectionStation(object):
	def __init__(self, station, datetime):
		self.station = station
		self.time = datetime.time()
		self.datetime = datetime

class HafasConnectionSection(object):
	pass

class HafasConnection(object):
	"""klasa przechowująca połączenie"""
	def __init__(self):
		pass

	@staticmethod
	def fromDOMElement(element):
		connection = HafasConnection()

		#overview

		def parseStation(element):
			stop, = element.getElementsByTagName('BasicStop')
			station, = stop.getElementsByTagName('Station')
			x = [stop.getElementsByTagName(x) for x in ('Dep', 'Arr')]
			arrdep, = x[0] + x[1]

			time = Hafas.parseTime(getText(arrdep.getElementsByTagName('Time')[0]))

			dt = datetime.combine(connection.date, time.time().min) + timedelta(0, time.second + time.minute * 60 + time.hour * 60 * 60 + (time.day - 1) * 24 * 60 * 60 )

			return HafasConnectionStation(HafasStation.fromDOMElement(station), dt)

		def parseSection(element):
			section = HafasConnectionSection()

			departure, = element.getElementsByTagName('Departure')
			arrival, = element.getElementsByTagName('Arrival')
			section.departure = parseStation(departure)
			section.arrival = parseStation(arrival)
			
			journey, = element.getElementsByTagName('Journey')
		
			def getAttributes(attributeList):
				attributes = {}
				for ja in attributeList.getElementsByTagName('JourneyAttribute'):
					attribute, = ja.getElementsByTagName('Attribute')
					name = ''
					if attribute.hasAttribute('type'):
						name = attribute.getAttribute('type')
					else:
						name = attribute.getAttribute('code')

					if len(name) == 2 and name[0] == 'P' and 48 <= ord(name[1]) <= 57:
						name = 'P0'

					value = ''
					for va in attribute.getElementsByTagName('AttributeVariant'):
						if va.getAttribute('type') == 'NORMAL':
							value = getText(va.firstChild)
							break

					attributes[name] = value
				return attributes

			attributeList, = journey.getElementsByTagName('JourneyAttributeList')
			attributes = getAttributes(attributeList)

			if 'P0' in attributes:
				operator = attributes['P0']
			else:
				operator = '??'
			type = attributes['CATEGORY']
			number = attributes['NUMBER']


			if 'P0' in attributes:
				attributes.pop('P0')
			attributes.pop('CATEGORY')
			attributes.pop('NUMBER')
			attributes.pop('OPERATOR')
			attributes.pop('NAME')

			section.train = HafasTrain(type, number, operator, attributes, section.departure, section.arrival)

			return section

		overview, = element.getElementsByTagName('Overview')
		connection.date = Hafas.parseDate(getText(overview.getElementsByTagName('Date')[0]))
		connection.duration = Hafas.parseTimeDelta(getText(overview.getElementsByTagName('Duration')[0].firstChild))

		connection.products = []
		products, = overview.getElementsByTagName('Products')

		#context, = overview.getElementsByTagName('ContextURL')
	
		#url, args = context.getAttribute('url').split('?')
		#args = dict(map(lambda x: x.split('=') if '=' in x else (x, True),  args.split('&')))
		
		#connection.ident = args['ident']

		for product in products.getElementsByTagName('Product'):
			connection.products.append(product.getAttribute('cat').strip())

		departure, = overview.getElementsByTagName('Departure')
		arrival, = overview.getElementsByTagName('Arrival')
		connection.departure = parseStation(departure)
		connection.arrival = parseStation(arrival)

		sectionlist, = element.getElementsByTagName('ConSectionList')

		connection.sections = []

		for section in sectionlist.getElementsByTagName('ConSection'):
			connection.sections.append(parseSection(section))

		return connection

	def toString(self):
		result = u'''<Connection
		From: {self.departure.station} ({self.departure.time})
		Destination: {self.arrival.station} ({self.arrival.time})
		Date: {self.date}
		Duration: {self.duration}
		Products: {self.products}

		Sections:
'''.format(self = self)
		for section in self.sections:
			result += u'''
			<Section
				From: {self.departure.station} ({self.departure.time})
				Destination: {self.arrival.station} ({self.arrival.time})
'''.format(self = section) + section.train.toString() + u'''
			>''';

		
		result += u'\n>'

		return result

	def queryStops(self):
		for section in self.sections:
			section.train.queryStops()

	def queryRelation(self, hafas = None):
		for section in self.sections:
			section.train.queryRelation(hafas = hafas)

	def approximateDistance(self):
		distance = 0.0
		for s in self.sections:
			distance += s.train.approximateDistance(self.departure.station, self.arrival.station)
			
		return distance
	
	def averageVelocity(self):
		return self.approximateDistance() / (self.duration.seconds / 3600.0)

class HafasTrain(object):
	"""klasa przechowująca trasę pociągu"""
	
	def __init__(self, type, number, operator, attributes, departure, arrival):
		self.type = type
		self.number = number
		self.operator = operator
		self.source = departure.station
		self.destination = arrival.station
		self.date = departure.datetime
		self.attributes = attributes
		self.stops_recorded = 0

#		self.queryStops()
		
	def toString(self):
		result = u'''
				<Train {self.type} {self.number}
					Operator: {self.operator}'''.format(self=self)
		
		if self.stops_recorded > 1:
			result += u'''
					Relation: {source} -- {destination}'''.format(source = self.relation_source(), destination = self.relation_destination())

		result += u'''
					Attributes'''.format(self = self)
		for code, text in self.attributes.items():
			result += u'''
						[{code}] {text}'''.format(code = code, text = text)

		if not self.stops_recorded > 0:
			result += u'''
					Stops: not queried'''
		else:
			result += u'''
					Stops:'''
			beetween = False
			for stop in self.stops:
				if stop.station == self.source:
					beetween = True

				if beetween:
					result += u'''
						{}'''.format(stop.toString())

				if stop.station == self.destination:
					beetween = False

		result += u'''\n
				>'''

		return result
	
	def queryStops(self, ident = None):
		if self.stops_recorded >= 1:
			return
		self.stops_recorded = 1
		self.stops = Hafas.getTrainStops(self.number, self.date, self.source, self.destination, ident)

	def queryRelation(self, ident = None, hafas = None):
		if hafas is None:
			hafas = Hafas
		if self.stops_recorded >= 2:
			return
		self.stops_recorded = 2
		self.stops = hafas.getTrainStops(self.number, self.date, self.source, self.destination, ident, True)
		
	def relation_source(self):
		if self.stops_recorded < 2:
			return None
		return self.stops[0].station

	def relation_departure(self):
		if self.stops_recorded < 2:
			return None
		return self.stops[0]

	def relation_destination(self):
		if self.stops_recorded < 2:
			return None
		return self.stops[-1].station

	def relation_arrival(self):
		if self.stops_recorded < 2:
			return None
		return self.stops[-1]

	def getId(self):
		sid = int("1{}{}{}".format(self.source.externalId, self.destination.externalId, self.date.strftime("%Y%m%d%H%M")))
		return "{:x}".format(sid)

	@staticmethod
	def connFromId(id, hafas = None):
		if hafas is None:
			hafas = Hafas
		if cache.in_cache(id):
			c = cache.load(id)
			return (c.sections[0].train, c)
		else:
			sid = "{}".format(int(id, 16))
			sourceId = sid[1:10]
			destinationId = sid[10:19]
			date = datetime.strptime(sid[19:], '%Y%m%d%H%M')
			source = HafasStation('dummy', sourceId, [])
			destination = HafasStation('dummy', destinationId, [])
			cl = hafas.searchConnections(source, destination, date,1)
	
			I = 10

			if datetime.combine(cl[-1].date, cl[-1].departure.time) != date:
				while datetime.combine(cl[-1].date, cl[-1].departure.time) < date:
		
					cl.next()
	
					if I == 0:
						break
					I -= 1
	
			c = cl[-1]
			c.queryRelation(hafas)

			cache.save(c, id)

			return (c.sections[0].train, c)

	@staticmethod
	def fromId(id):
		t, _ = HafasTrain.connFromId(id)
		return t

	def approximateDistance(self, source = None, destination = None):
		def gskID(s):
			return Station.search(s).gskID

		before = None
		count = False
		if source is None:
			count = True
		distance = 0.0

		for stop in self.stops:
			if before is None:
				before = stop
				stop.fromStart = 0.000
				continue

			if before.station == source:
				count = True

			if count:
				distance += Dijkstra.length(stop.station.gskID(), before.station.gskID())
				stop.fromStart = distance

			if stop.station == destination:
				count = False

			before = stop

		return distance

MINUTE = timedelta(minutes = 1)

class HafasStop(object):
	"""klasa przechowująca postój"""

	def __init__(self):
		self.arrival = None
		self.departure = None
		self.station = None
		

	@staticmethod
	def fromDOMElement(element):
		stop = HafasStop()
		if element.hasAttribute('arrTime'):
			stop.arrival = Hafas.parseTime(element.getAttribute('arrTime')).time()
		if element.hasAttribute('depTime'):
			stop.departure = Hafas.parseTime(element.getAttribute('depTime')).time()

		stop.station = HafasStation.fromDOMElement(element, 'evaId')


		return stop

	def toString(self):
		def __(x):
			return u"     " if x is None else x.strftime("%H:%M")
		return u"{name:<40} {arr} {dep}".format(name = self.station.name, arr = __(self.arrival), dep = __(self.departure))

	def __repr__(self):
		return self.toString()

	def is_long(self):
		def todt(t):
			return datetime.combine(date.today(), t)

		if self.departure is None or self.arrival is None:
			return False

		diff = todt(self.departure) - todt(self.arrival)

		return diff > MINUTE

	def is_short(self):
		if self.departure is None or self.arrival is None:
			return False
		return not self.is_long()

class HafasObject(object):
	"""klasa służąca do komunikacji z Hafasem"""

	_connection = None
	
	@staticmethod
	def parseDate(datestr):
		return datetime.strptime(datestr, "%Y%m%d").date()

	@staticmethod
	def parseTime(timestr):
		if 'd' in timestr:
			d, x = timestr.split('d')
		else:
			d, x = '0', timestr
		if len(x) == 8:
			date = datetime.strptime(x, "%H:%M:%S")
		else:
			date = datetime.strptime(x, "%H:%M")

		if d == '1':
			date += timedelta(1)
		return date

	@staticmethod
	def parseTimeDelta(timestr):
		date = Hafas.parseTime(timestr)
		return timedelta(0, date.second + date.minute * 60 + date.hour * 60 * 60 + (date.day - 1) * 60 * 60 * 24)

	def _getConnection(cls, can_reuse = True):
		if cls._connection == None or not can_reuse:
			cls._connection = httplib.HTTPConnection('rozklad-pkp.pl')

		return cls._connection

	def searchStation(cls, station):
		result, = cls.searchStations([station])
		return result

	def searchStations(cls, stations, verbose = False):
		"""dzieli stations na paczki po N"""
		N = 10
		result = []
		for i in range(len(stations)/N+1):
			result.extend(cls._searchStations(stations[i*N:(i+1)*N]))

		return result

	def _searchStations(cls, stations):
		"""próbuje znaleźć stacje o podanych nazwach
		jest niedeterministyczne!
		czasami dla zapytania 'Radom' zwraca 'Radomyśl', a czasami nie
		
		"""

		if len(stations) == 0:
			return []
		
		request  = u'<?xml version="1.0" encoding="utf-8" ?>'

		id = 1

		for station in stations:
			request += u'<LocValReq id="{id:0>3}"><ReqLoc type="ST" match="{station}" /></LocValReq>'.format(id = id, station = station.decode('utf-8'))
			id += 1

		data = cls._performRequest(request)


		dom = parseString(data)

		result_map = {}

		for response in dom.getElementsByTagName('LocValRes'):
			id = int(response.getAttribute('id'))
			query_result = []
			for element in response.getElementsByTagName('Station'):
				query_result.append(HafasStation.fromDOMElement(element))
			
			result_map[id-1] = query_result


		result = [result_map[id] for id, _ in enumerate(stations)]
		return result

	def _performRequest(cls, request, xml = True, exe = None):
		connection = cls._getConnection()
		addr = '/bin/stboard.exe/pn'
		if xml:
			request = u'<?xml version="1.0" encoding="utf-8"?><ReqC ver="1.1" prod="String" lang="PL">{}</ReqC>'.format(request)
			addr = '/bin/query.exe/pn'
		
		if exe is not None:
			addr = '/bin/{}/pn'.format(exe)

		try:
			connection.request("POST", addr, request.encode('utf-8'), {'Content-Type': 'text/xml; charset=utf-8'})
			response = connection.getresponse()
		except (httplib.CannotSendRequest, httplib.BadStatusLine) :
			connection = cls._getConnection(False)
			connection.request("POST", addr, request.encode('utf-8'), {'Content-Type': 'text/xml; charset=utf-8'})
			response = connection.getresponse()


		if response.status != 200:
			raise HafasError('HTML', '{} {}'.format(response.status, response.reason))
		data = response.read()

		if not xml:
			data = u'<Response>{data}</Response>'.format(data=data)

		try:
			dom = parseString(data)
		except:
			raise

		errs = dom.getElementsByTagName('Err')
		for err in errs:
			code = err.getAttribute('code')
			text = err.getAttribute('text')
			level = err.getAttribute('level')

			if level == 'E':
				raise HafasError(code, text)
			
			if level == 'W':
				if code == 'K1:890':
					continue
				raise HafasWarning(code, text)
	
			raise HafasException(code, text)

		return data

	
	def searchConnections(cls, source, destination, datetime, number = 3, departure = True, via = None, only_direct = True):
		connection = cls._getConnection()
		request = u'<ConReq>'
		request += u'<Start>'
		request += source.toHafasString()
		request += u'<Prod prod="{prod}" bike="0" couchette="0" direct="{direct}" sleeper="0"/>'.format(direct = 1 if only_direct else 0, prod = '1' * 16)
		request += u'</Start>'
		if via is not None:
			request += u'<Via>'
			request += via.toHafasString()
			request += u'<Prod prod="{prod}" bike="0" couchette="0" direct="0" sleeper="0"/>'.format(prod = '1'*16)
			request += u'</Via>'
		request += u'<Dest>'
		request += destination.toHafasString()
		request += u'</Dest>'
		request += u'<ReqT a="{departure}" date="{date}" time="{time}" />'.format(departure = 0 if departure else 1, date = datetime.strftime("%Y.%m.%d"), time = datetime.strftime("%H:%M"))
		request += u'<RFlags b="0" chExtension="0" f="{number}" />'.format(number = number)
		request += u'</ConReq>'

		data = cls._performRequest(request)

		dom = parseString(data)

		return HafasConnectionList.fromDOMElement(dom)

	def getMoreConnections(cls, context, number):
		request  = u'<ConScrReq src="F" nrCons="{number}">'.format(number = number)
		request += u'<ConResCtxt>{context}</ConResCtxt>'.format(context = context)
		request += u'</ConScrReq>'

		data = cls._performRequest(request)

		dom = parseString(data)

		return HafasConnectionList.fromDOMElement(dom)

	def searchConnectionsByDate(cls, source, destination, date = None, only_direct = True, tomorrow = None):
		if date is None:
			date = datetime.now().date()

		date = datetime.combine(date, time.min) + timedelta(0,60)
		if tomorrow is None:
			tomorrow = datetime.combine(date + timedelta(1), time.min)

		connectionList = cls.searchConnections(source, destination, date, 6, only_direct = only_direct)

		while connectionList[-1].departure.datetime < tomorrow:
			connectionList.next()

		while connectionList[-1].departure.datetime >= tomorrow:
			connectionList.pop()

		while connectionList[0].departure.datetime < date:
			connectionList.pop(0)

		return connectionList

	def getTrainStops(cls, trainNumber, datetime, source, destination, ident, all = False):
		post = {
				'start': 'yes',
#				'REQTrain_name': trainNumber,
				'date': datetime.strftime('%d.%m.%Y'),
				'time': datetime.strftime('%H:%M'),
#				'date': 'today',
#				'time': 'now',
				'sTI': 1,
#				'ident': ident,
				'board_type': 'dep',
				'L': 'vs_java3',
				'dirInput': destination.externalId,
				'input': source.externalId,
#				'ld': 'hw1',
				}


		data = cls._performRequest(urllib.urlencode(post), False)
		dom = parseString(data)

		result = []

		beetween = False

		for elem in dom.getElementsByTagName('St'):
	
			stop = HafasStop.fromDOMElement(elem)
			if stop.station == source:
				beetween = True

			if beetween or all:
				result.append(HafasStop.fromDOMElement(elem))

			if stop.station == destination:
				beetween = False

		return result

Hafas = HafasObject()

if __name__ == '__main__':
	from datetime import datetime, timedelta
#	(kutno,) , (radom,) =  Hafas.searchStations([u"Warszawa Wschodnia".encode('utf-8'), u"5100010".encode('utf-8')])

#	cl = Hafas.searchConnections(kutno, radom, datetime.now().date(), only_direct = True, number=3)
	

	x = Hafas.searchStations([u'Boleszewo'])

#	c = cl[0]

#	c.queryRelation()

#	print c.toString()

#	print Hafas.getTrainStops(62122, None, kutno, kutno)
	
