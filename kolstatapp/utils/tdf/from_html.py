import yaml
import sys
import re
import HTMLParser

h = HTMLParser.HTMLParser()

name = sys.argv[1]

op = name
num = ''

while op[-1].isdigit():
	num = op[-1:] + num
	op = op[:-1]

good_name = op + ' ' + num

with open(name + '.html') as f:
	s = h.unescape(f.read())

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
document['name'] = good_name

from datetime import date

oper = dict()
oper['mode'] = 'single'
oper['date'] = date(2013, 1, 3)
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

print yaml.dump(document)