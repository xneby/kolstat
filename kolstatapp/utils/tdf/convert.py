#!/usr/bin/env python2

import sys
import yaml
from pprint import pprint
from datetime import date

def convert_file(filename):
	with open(filename) as f:
		data = f.read()

	y = yaml.load(data)

	y['operations'][0]['mode'] = 'interval'
	y['operations'][0]['from'] = date(2013, 2, 6)
	y['operations'][0]['to'] = date(2013, 2, 6)

	output = yaml.dump(y)

	with open(filename, "w") as f:
		f.write(output)

for x in sys.argv[1:]:
	print x
	convert_file(x)
