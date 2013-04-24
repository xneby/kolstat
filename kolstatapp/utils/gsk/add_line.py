#!/usr/bin/env python2

import sys
nr = int(sys.argv[1])
import http.client
import re
from .add_edge import add_edge
from .add_vertex import add_vertex

conn = http.client.HTTPConnection('bazakolejowa.pl')

conn.request('GET', '/index.php?dzial=linie&id={}&okno=przebieg'.format(nr))

resp = conn.getresponse()

print(resp.status, resp.reason)
data = resp.read()

REG = r'''[[]id[]] => ([0-9]*)
.*?[[]nazwa[]] => .*
.*?[[]typ[]] => .*
.*?[[]wojewodztwoID[]] => .*
.*?[[]wojewodztwo[]] => .*
.*?[[]GPS[]] => .*
.*?[[]skala[]] => .*
.*?[[]km[]] => ([0-9]*(?:\.[0-9]*)?)
'''
print(data)

ll = re.findall(REG,data,re.MULTILINE)

for (v1, km1), (v2, km2) in zip(ll, ll[1:]):
	v1 = int(v1)
	v2 = int(v2)
	km1 = float(km1)
	km2 = float(km2)

	add_vertex(v1)
	add_vertex(v2)
	add_edge(v1, v2, float(km1-km2))
