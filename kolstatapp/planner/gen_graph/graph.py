from kolstatapp.models import Station
from kolstatapp.utils.kolstat_time import make_planner_time
from pprint import pprint
import sys
import time
import struct
import datetime

MAGIC, = struct.unpack('i', 'TTF0')
DZIEN = datetime.timedelta(days = 1)

def info(s):
	sys.stdout.write('\r' + s)
	sys.stdout.flush()

def done(s = '', t = None):
	if s != '':
		sys.stdout.write('\033[2K\r')
	if t is None:
		x = ''
	else:
		x = '{:.2f}'.format(time.time() - t)
	print '{}done. (t = {})'.format(s,x)

class Graph(object):

	def __init__(self, *args, **kwargs):
		self.build()

	def get_query_result(self):
		from django.db import connection
		cursor = connection.cursor()

		cursor.execute("""SELECT t1.station_id, t1.departure, t1.departure_overnight, t2.arrival, t2.arrival_overnight, t2.station_id, t1.id, t2.id, tt.date
		                  FROM kolstatapp_trainstop AS t1
		                  JOIN kolstatapp_trainstop AS t2 ON t1.order + 1 = t2.order
		                  JOIN kolstatapp_traintimetable AS tt ON t1.timetable_id = tt.id
		                  WHERE t1.timetable_id = t2.timetable_id""")

		return cursor.fetchall()

	def make_station_list(self):
		stations = Station.objects.order_by('-pk')
		result = [None] * (stations[0].pk + 1)

		for st in stations:
			result[st.pk] = st

		return result
	
	def make_datetime(self, date, time, overnight):
		res = datetime.datetime.combine(date, time)
		if overnight:
			res += DZIEN
		return res

#	def make_connection(self, stop1, stop2):
	def make_connection(self, st1, dep, ts1, st2, arr, ts2):
		source = st1
		dest = st2
		result = None

		if (source, dest) not in self.connections:
			self.list_conn.append((source, dest))
			result = len(self.list_conn)
			self.connections[(source, dest)] = []

		connection = (source, dest, dep, arr, ts1, ts2)

		self.connections[(source,dest)].append(connection)
		return result			

	def build(self):
		self.stations = self.make_station_list()
		self.edges = dict()
		
		for x in range(1, len(self.stations)+1):
			self.edges[x] = []

		self.connections = dict()
		self.list_conn = []

		#
		info('Querying...')
		start_time = time.time()
		query_result = self.get_query_result()
		done('Querying...', start_time)
	
		l = len(query_result)

		start_time = time.time()
		for i, (st1, dep, depon, arr, arron, st2, ts1, ts2, date) in enumerate(query_result):
			if i % 128 == 0:
				info('Generating graph... {:4}/{} ({:6.2f}%)'.format(i, l, 100.0*i/l))
			
			nr = self.make_connection(st1, self.make_datetime(date, dep, depon), ts1, st2, self.make_datetime(date, arr, arron), ts2)
			if nr is not None:
				self.edges[st1].append((st2, nr))

		done('Generating graph... ', start_time)
	
		conn = sum(len(v) for k, v in self.connections.items()) 
		vertices = sum(1 for k, v in self.edges.items() if len(v) > 0)
		edges = sum(len(v) for k, v in self.edges.items()) 

		print 'Parameters: C={} V={} E={}'.format(conn, vertices, edges)

	def save_to(self, stream):
		class Buffer:
			length = 0

			@classmethod
			def append(cls, s):
				stream.write(s)
				cls.length += len(s)

		def write_integer(n):
			Buffer.append(struct.pack('i', n))
		
		def write_string(s):
			Buffer.append(s)

		start_time = time.time()
		info('Writing header... ')

		write_integer(MAGIC)
		write_integer(time.time())

		write_integer(len(self.stations))
		write_integer(len(self.list_conn))

		done(t = start_time)

		start_time = time.time()
		info('Writing stations... ')
		l = len(self.stations)
		for i, st in enumerate(self.stations):
			info('Writing stations... {:3}/{:3} ({:6.2f}%) '.format(i, l, 100.0 * i/l))
			if st is None or st.pk not in self.edges:
				write_integer(0)
			else:
				conn = self.edges[st.pk]
				write_integer(len(conn))
				for st, nr in conn:
					write_integer(st)
					write_integer(nr)

		done('Writing stations... ', start_time)

		start_time = time.time()
		l = len(self.list_conn)
		for i, (s1, s2) in enumerate(self.list_conn):
			info('Writing connections... {:3}/{:3} ({:6.2f}%) '.format(i, l, 100.0 * i/l))
			conns = self.connections[(s1, s2)]
			write_integer(len(conns))
			for s, d, dt, at, s1, s2 in conns:
				write_integer(s)
				write_integer(d)
				write_integer(make_planner_time(dt))
				write_integer(make_planner_time(at))
				write_integer(s1)
				write_integer(s2)
		
		done('Writing connections... ', start_time)

		print 'size: {}KiB'.format(Buffer.length/1024)

		pprint(sorted(self.connections[self.list_conn[336]], lambda x,y: cmp(x[2], y[2])))

#		stream.write(Buffer._buffer)
