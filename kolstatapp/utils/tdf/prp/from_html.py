#coding: utf-8
import yaml
import sys
import re
try:
	import html.parser
except ImportError:
	import html.parser as HTMLParser

h = html.parser.HTMLParser()

'''<td class="nowrap sepline">
<a href="http://rozklad.sitkol.pl/bin/stboard.exe/pn?ld=c&time=19:23&input=5101097&boardType=dep&productsFilter=1111111&">Gorzów Chrzanowski</a>
</td>
<td class="center sepline">
19:22
</td>
<td class="center sepline">
19:23
</td>'''

def parse(s, name, dd, var):

	ll = re.findall(r'''<td class="nowrap sepline">
<a href="[^"]*">([^<]*)</a>
</td>
<td class="center sepline">
([^<]*)
</td>
<td class="center sepline">
([^<]*)
</td>''', s, re.MULTILINE | re.DOTALL)

	name=re.sub('([A-Z])([0-9])', r'\1 \2', name)

	document = dict()
	document['type'] = 'train'
	document['mode'] = 'normal'
	document['name'] = name
	document['variant'] = var

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

	print(parse(s, good_name, date(2013,2,4)))
