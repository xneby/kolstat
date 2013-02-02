from django.conf import settings
from kolstatapp.utils.kolstat_time import make_planner_time
from kolstatapp.models import TrainStop
import struct
import socket
import errors
from lazy import lazy
import logging

class SimpleQuery:
	@staticmethod
	def to_s(source_st, dest_st, time):
		ss = source_st.pk
		dd = dest_st.pk

		tt = make_planner_time(time)

		print ss,dd,tt
		
		return struct.pack("iiii", 1, ss, dd, tt)

def ask(to_send):
	s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	s.connect(settings.INSTALL_DIR + '/kolstatapp/planner/planner_socket')
	s.sendall(to_send)
	answer = ''
	while True:
		data = s.recv(1024)
		if not data: 
			break
		answer += data
	
	s.close()
	return answer

def expand_stops(inp):
	ll = set()
	for conn in inp:
		for x,y in conn:
			ll.add(x)
			ll.add(y)
	stops = TrainStop.objects.filter(pk__in = ll).select_related()
	dd = dict()
	for st in stops:
		dd[st.pk] = st
	result = []
	for conn in inp:
		result.append([])
		for x,y in conn:
			result[-1].append((dd[x], dd[y]))
	return result

def make_simple_query(source_st, dest_st, time):
	to_send = SimpleQuery.to_s(source_st, dest_st, time)
	answer = ask(to_send)
	
	t, = struct.unpack_from('i', answer, 0)

	if t == 1:
		type, length = struct.unpack_from('ii', answer, 4)
		message = answer[12:12+length]

		if type == 0:
			raise errors.ErrorUndefined(message)
		elif type == 1:
			raise errors.ErrorNotImplemented(message)
		elif type == 2:
			raise errors.ErrorBadRequest(message)
		else:
			raise errors.ErrorProtocolError('Bad error type.')
	elif t == 0:
		count, = struct.unpack_from('i', answer, 4)
		elapsed = 8
		result = []
		
		for i in range(count):
			length, = struct.unpack_from('i', answer, elapsed)
			elapsed += 4
			conn = []
			for j in range(length):
				s1, s2 = struct.unpack_from('ii', answer, elapsed)
				elapsed += 8
				conn.append((s1, s2))
			result.append(conn)
			stats = struct.unpack_from('iii', answer,elapsed)
			elapsed += 12
	
			logging.info('DIJKSTRA V = {}, H = {}, P = {}'.format(*stats))
		return expand_stops(result)
