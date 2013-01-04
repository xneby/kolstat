#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from hafas import Hafas
from sys import argv
def main(inf, ouf):
	with open(inf) as f:
		stacje = []
		for l in f:
			nazwa, numer = map(str.strip, l.split('\t'))
			numer = int(numer)

			stacje.append((nazwa.decode('utf-8'), numer))

	print "Wysyłanie zapytania"
	odpowiedz = Hafas.searchStations([x for x,y in stacje], True)
	print "Otrzymano odpowiedź"

	with open(ouf, 'w') as f, open('log', 'w') as l:
		for stacje, nazwa, numer in zip(odpowiedz, *zip(*stacje)):
			if len(stacje) == 1:
				stacja, = stacje
				f.write('{},{},{}\n'.format(nazwa.encode('utf-8'), numer, stacja.externalId))
			elif len(stacje) == 0:
				l.write('{} FAIL\n'.format(nazwa.encode('utf-8')))
			else:
				stacja = stacje[0]
				if stacja.name != nazwa:
					l.write('{} FAIL\n'.format(nazwa.encode('utf-8')))
					continue
				f.write('{},{},{}\n'.format(nazwa.encode('utf-8'), numer, stacja.externalId))



if __name__ == '__main__':
	if len(argv) > 1:
		inf = argv[1]
	else:
		inf = 'kurs90.numery'
	if len(argv) > 2:
		ouf = argv[2]
	else:
		ouf = 'kurs90.output'
	main(inf, ouf)
