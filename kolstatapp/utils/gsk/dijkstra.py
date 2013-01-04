#!/usr/bin/env python3
# coding: utf-8
import heapq
import pickle
import os.path

rs = {}
s = {}
kr = {}

DIR, _ =  os.path.split(os.path.abspath(__file__))

if __name__ == '__main__':
	with open('nrid2') as f:
		for l in f:
			a, b = l.strip().split('::')
			a = int(a)
			rs[b] = a
			s[a] = b

	def add(a,b,c):
		a = int(a)
		b = int(b)
		c = float(c)
		if a not in kr:
			kr[a] = []
		kr[a].append((b,c))

	with open('kraw') as f:
		for l in f:
			a, b, c = l.strip().split()
	
			add(a,b,c)
			add(b,a,c)
else:
	with open(os.path.join(DIR, 'kraw.p'), 'rb') as f:
#	with open('kraw.p', 'wb') as f:
		kr = pickle.load(f)
#		pickle.dump(kr,f)

class Dijkstra:
	mem = {}
	
	@classmethod
	def dijkstra(cls, f, to):
		if f not in cls.mem:
			cls.mem[f] = cls._dijkstra(f, to)
		
	@classmethod
	def length(cls, f, to):
		cls.dijkstra(f,to)
		return cls.mem[f]['d'][to]

	@classmethod
	def path(cls, f, to):
		cls.dijkstra(f,to)
		t = [to]
		while t[-1] != f:
			t.append(cls.mem[f]['p'][t[-1]])

		return reversed(t)
	
	@classmethod
	def _dijkstra(cls, f, to):
		d = {}
		p = {}

		d[f] = 0
		p[f] = None

		heap = [f]

		while heap:
			v = heapq.heappop(heap)

			for u,c in kr[v]:
				if u not in d or d[u] > d[v] + c:
					d[u] = d[v] + c
					p[u] = v

					heapq.heappush(heap, u)

		return dict(d=d, p=p)

if __name__ == '__main__':
	start = ''
	end = ''
	print('Podaj stacje:')
	while start not in rs:
		start = input('Start: ')
	while end not in rs:
		end = input('Koniec: ')
	si = rs[start]
	ei = rs[end]

	l, p = Dijkstra.length(si, ei), Dijkstra.path(si,ei)

	print('Odległość:', l)

	print("Stacje:")
	for i in p:
		print(s[i])
