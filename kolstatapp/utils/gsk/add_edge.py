#!/usr/bin/env python2
import pickle
import sys

def add_edge(v1, v2, c):
	with open('kraw.p') as f:
		a = pickle.load(f)

	for v, c in a[v1]:
		if v == v2:
			print(c)
			return

	a[v1].append((v2, c))
	a[v2].append((v1, c))

	with open('kraw.p', 'w') as f:
		pickle.dump(a,f)

if __name__ == '__main__':
	v1 = int(input('v1 '))
	v2 = int(input('v2 '))
	c = abs(float(input('c ')))/1000.0
	add_edge(v1, v2, c)
