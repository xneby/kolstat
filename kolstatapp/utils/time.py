from datetime import timedelta

def time_diff(a, b):
	def mm(x):
		return x.hour * 60 + x.minute
	m = mm(a) - mm(b)
	
	return timedelta(minutes = m)

def hours(t):
	return t.total_seconds() / 3600
