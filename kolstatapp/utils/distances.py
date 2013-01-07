def get_distance(start, end):
	if start.timetable == end.timetable:
		return abs(start.distance - end.distance)
	else:
		raise ValueError('Not the same timetable')