import oferty
from kolstatapp.utils.distances import get_distance

class InvalidConnection(Exception): pass

import pprint

def calculate(plan, discounts):

	def _price(op):
		return sum(map(lambda x: x[-1], op))

	def _get_oplaty(plan):
		result = []
		#pprint.pprint(plan)
		for of in oferty.oferty:
			distance = 0.0
			valid = True
			tmp_result = [] 
			first_start = None
			last_end = None
			for train, start, end in plan:
				if not of.is_valid(train, start, end):
					valid = False
				tmp_result.extend( ('additional', of, type, train, znizka, value) for type, value, znizka in of.get_additional_prices(train, discounts))
				distance += get_distance(start, end)
				last_end = end
				if first_start is None:
					first_start = start

			if valid:
				tmp_result.extend(('base', of, type, (first_start, last_end), znizka, value) for type, value, znizka in of.get_base_price(distance, discounts))

				if result == [] or _price(result) > _price(tmp_result):
					result = tmp_result

		#pprint.pprint(result)
		if result == []:
			raise InvalidConnection()
		return result

	oplaty = [[] for x in plan]

	for i, _ in enumerate(plan):
		j = 0
		while j <= i:

			try:
				tmp_oplata = ([] if j == 0 else oplaty[j-1]) + _get_oplaty(plan[j:i+1])
				print j, i
				pprint.pprint(tmp_oplata)
				if oplaty[i] == [] or _price(oplaty[i]) > _price(tmp_oplata):
					oplaty[i] = tmp_oplata
			except InvalidConnection:
				pass

			j += 1 

	return oplaty[-1]
	
def calc_price(op):
	return sum(map(lambda x: x[-1], op))

def plan_from_connection(conn):
	plan = []
	for s in conn.sections:
		plan.append((s.train, s.stops[0], s.stops[-1]))
	return plan
