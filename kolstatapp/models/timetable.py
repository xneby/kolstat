from django.db import models
from datetime import datetime, date, timedelta
from kolstatapp.utils.kolstat_time import time_diff, hours

class TrainTimetable(models.Model):
	train = models.ForeignKey('kolstatapp.Train')
	date = models.DateField()

	class Meta:
		app_label = 'kolstatapp'

	def first_stop(self):
		return self.trainstop_set.get(order = 1)

	def last_stop(self):
		return self.trainstop_set.order_by('-order')[0]

	def approximate_distance(self):
		return self.last_stop().distance

	def duration(self):
		return time_diff(self.last_stop().arrival, self.first_stop().departure)

	def average_velocity(self):
		return self.approximate_distance() / hours(self.duration())

	def stops(self):
		return self.trainstop_set.order_by('order').select_related()

	def get_coupled(self):
		return [x.stop1.timetable for x in TrainCouple.objects.filter(stop2__in = self.stops())]

	def get_couplings(self, after = 0):
		return [(x.stop1.timetable, x.stop1.order) for x in TrainCouple.objects.filter(stop2__in = self.stops()).filter(stop2__order__gt = after)]

	def get_stations_id(self):
		return self.trainstop_set.values_list('station__id', flat=True)

	def interval(self, s1, s2):
		o1 = self.trainstop_set.get(station = s1).order
		o2 = self.trainstop_set.get(station = s2).order
		print(s1,s2,o1,o2)

		return self.trainstop_set.filter(order__gte = o1).filter(order__lte = o2).order_by('order')

	def __str__(self):
		return "{} ({})".format(self.train, self.date)

class TrainStop(models.Model):
	timetable = models.ForeignKey(TrainTimetable)
	station = models.ForeignKey('kolstatapp.Station')
	arrival = models.DateTimeField(null = True)
	departure = models.DateTimeField(null = True)

	track = models.CharField(max_length = 10, null = True)
	platform = models.CharField(max_length = 10, null = True)
	
#	arrival_overnight = models.IntegerField(null = True)
#	departure_overnight = models.IntegerField(null = True)

	distance = models.FloatField()

	order = models.IntegerField()

	def is_dummy(self):
		return self.arrival is None and self.departure is None

	def is_short(self):
		if self.stop_duration() is None:
			return False
		return self.stop_duration() <= timedelta(minutes = 1)

	def stop_duration(self):
		if self.arrival is None or self.departure is None:
			return None
		if self.departure < self.arrival:
			return time_diff(self.departure,  self.arrival) + timedelta(day=1)
		return time_diff(self.departure, self.arrival)

	def __next__(self):
		try:
			return self.timetable.trainstop_set.get(order = self.order + 1)
		except TrainStop.DoesNotExist:
			return None

	def departure_datetime(self):
#		if self.departure is None: return None
#		return datetime.combine(self.timetable.date, self.departure) + timedelta(days = self.departure_overnight or 0)
		return self.departure

	def arrival_datetime(self):
#		if self.arrival is None: return None
#		return datetime.combine(self.timetable.date, self.arrival) + timedelta(days = self.arrival_overnight or 0)
		return self.arrival

	def to_json(self):
		return dict(station = self.station.to_json(), arrival = self.arrival_datetime(), departure = self.departure_datetime(), distance = self.distance)

	class Meta:
		app_label = 'kolstatapp'

	def __str__(self):
		return "{} @ {} ({} - {})".format(self.timetable, self.station, self.arrival, self.departure)

class TrainCouple(models.Model):
	stop1 = models.ForeignKey(TrainStop, related_name = 'couple1')
	stop2 = models.ForeignKey(TrainStop, related_name = 'couple2')

	class Meta:
		app_label = 'kolstatapp'

