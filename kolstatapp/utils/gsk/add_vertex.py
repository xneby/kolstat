#!/usr/bin/env python2
import pickle

def add_vertex(nr):
	with open('kraw.p') as f:
		a = pickle.load(f)

	try:
		print(a[nr])
	except KeyError:
		a[nr] = []
		print('added')

	with open('kraw.p', 'w') as f:
		pickle.dump(a,f)

if __name__ == '__main__':
	t = int(input('Nr: '))
	add_vertex(t)
