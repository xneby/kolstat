#!/usr/bin/env python2
import pickle

with open('kraw.p') as f:
	a = pickle.load(f)

v1 = int(input('v1 '))
v2 = int(input('v2 '))

a[v1]= [(v, c) for v,c in a[v1] if v != v2]
a[v2]= [(v, c) for v,c in a[v2] if v != v1]

with open('kraw.p', 'w') as f:
	pickle.dump(a,f)
