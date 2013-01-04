from django.db import models
from datetime import datetime, date, timedelta
from kolstatapp.utils.time import time_diff, hours

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
		return self.trainstop_set.order_by('order')

	def get_coupled(self):
		return map(lambda x: x.stop1.timetable, TrainCouple.objects.filter(stop2__in = self.stops()))

	def get_couplings(self, after = 0):
		return map(lambda x: (x.stop1.timetable, x.stop1.order), TrainCouple.objects.filter(stop2__in = self.stops()).filter(stop2__order__gt = after))

	def __unicode__(self):
		return u"{} ({})".format(self.train, self.date)

class TrainStop(models.Model):
	timetable = models.ForeignKey(TrainTimetable)
	station = models.ForeignKey('kolstatapp.Station')
	arrival = models.TimeField(null = True)
	departure = models.TimeField(null = True)
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

	class Meta:
		app_label = 'kolstatapp'

	def __unicode__(self):
		return u"{} @ {}".format(self.timetable, self.station)

class TrainCouple(models.Model):
	stop1 = models.ForeignKey(TrainStop, related_name = 'couple1')
	stop2 = models.ForeignKey(TrainStop, related_name = 'couple2')

	class Meta:
		app_label = 'kolstatapp'

