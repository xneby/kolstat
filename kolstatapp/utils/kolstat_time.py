from datetime import timedelta
from django.conf import settings

def time_diff(a, b):
	def mm(x):
		return x.hour * 60 + x.minute
	m = mm(a) - mm(b)
	
	return timedelta(minutes = m)

def hours(t):
	return t.total_seconds() / 3600

def make_planner_time(time):
	td = time - settings.TIMETABLE_START
	return td.seconds // 60 + td.days * 60*24
