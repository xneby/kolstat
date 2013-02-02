import yaml
import sys
import re
try:
	import HTMLParser
except ImportError:
	import html.parser as HTMLParser

h = HTMLParser.HTMLParser()

def parse(s, name, dd):

	ll = re.findall(r'''<td class="nowrap sepline">
	<a href=".*?">(.*?)</a>
	</td>
	<td class="center sepline">
	(.*?)
	</td>
	<td class="center sepline">
	(.*?)
	</td>''', s, re.MULTILINE | re.DOTALL)

	document = dict()
	document['type'] = 'train'
	document['mode'] = mode
	document['name'] = name
	
	from datetime import date

	oper = dict()
	oper['mode'] = 'single'
	oper['date'] = dd
	tt = []
	for s, a, d in ll:
		td = dict()
		td['station'] = s
		if ':' in a:
			td['arrival'] = a
		if ':' in d:
			td['departure'] = d
		tt.append(td)

	oper['timetable'] = tt
	
	document['operations'] = [oper]
	
	return yaml.dump(document)

if __name__ == '__main__':
	name = sys.argv[1]

	try:
		mode = sys.argv[2]
	except IndexError:
		mode = 'normal'

	op = name
	num = ''

	while op[-1].isdigit():
		num = op[-1:] + num
		op = op[:-1]

	good_name = op + ' ' + num

	with open(name + '.html') as f:
		s = h.unescape(f.read())

	print(parse(s, good_name, date(2013,2,4))
