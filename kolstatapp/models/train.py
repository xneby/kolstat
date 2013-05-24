# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from kolstatapp.models import Composition, Station, TrainTimetable, TrainCategory, TrainStop
from django.db.models.aggregates import Avg, Count

#from kolstatapp.utils.normal_to_hafas import get_relation, getId, acquire, save_cache
from kolstatapp.utils import cache
from kolstatapp.exceptions import KolstatError

class Train(models.Model):
	category = models.ForeignKey('kolstatapp.TrainCategory')
	number = models.CharField(max_length = 7)
	variant = models.CharField(max_length = 1)
	
	source = models.ManyToManyField(Station, related_name = 'train_source')
	destination = models.ManyToManyField(Station, related_name = 'train_destination')
	
	def to_json(self):
		return dict(id = self.id, operator = self.category.operator.name, category = self.category.name, number = self.number)

	@models.permalink
	def get_absolute_url(self):
		if self.has_variants():
			return ('kolstat-train-variant', [self.category.name, self.number, self.variant])
		else:
			return ('kolstat-train', [self.category.name, self.number])

	def timetables(self):
		return self.traintimetable_set.order_by('date')

	def delete_train(self):
		for tt in self.timetables():
			cache.delete(tt.timetable)
		self.delete()

	def has_variants(self):
		if hasattr(self, '_has_variants'):
			return self._has_variants
		else:
			self._has_variants = len(Train.objects.filter(category = self.category, number = self.number)) > 1
			return self._has_variants

	@staticmethod
	def in_hafas(oper, number, connection = None, hafas = None):
		name = '{} {}'.format(oper.name, number)
		#xx = acquire(name, connection)

		#if len(xx.keys()) == 0:
		#	return False

		return True

	@staticmethod
	def add_train(name, connection = None, hafas = None, template = None):
		if ' ' in name:
			oper, number = name.split(' ')

			try:
				oper = TrainCategory.objects.get(name = oper)
			except TrainCategory.DoesNotExist:
				raise KolstatError('Brak takiej kategorii')

			if oper.name == 'R':
				name = number

		else:
			raise KolstatError('Brak kategorii pociągu')

		tt = Train.search(name)
		if len(tt) > 0:
			raise KolstatError('Pociąg istnieje w bazie')
		else:
			
			if len(list(xx.keys())) == 0:
				raise KolstatError('Brak pociągu w Hafasie')
			
			for k, v in list(xx.items()):
				if template is None:
					t = Train(category = oper, number = int(number))
				else:
					t = template
					template = None

				t.save()

				t.variant = k

				t.update_relation(v['source'], v['destination'])
				t.get_timetable(v['ids'])
				t.save()

			return t

	def get_timetable(self, ids = None):
		to_add = []
		for k,v in list(ids.items()):
			tt = TrainTimetable(train = self, date = k, timetable = v)
			to_add.append(tt)

			if len(to_add) > 100:
				TrainTimetable.objects.bulk_create(to_add)
				to_add = []
		TrainTimetable.objects.bulk_create(to_add)

	def update_relation(self, s = None, d = None):
		
		self.source = [ Station.objects.get(hafasID = x) for x in s]
		self.destination = [ Station.objects.get(hafasID = x) for x in d]

		self.save()

	@staticmethod
	def search(name, variant = None):
		if ' ' in name:
			list = name.split(' ')

			if len(list) == 2:
				oper, number = list
			else:
				oper, number, variant = list

			try:
				oper = TrainCategory.objects.get(name = oper)
			except TrainCategory.DoesNotExist:
				return []

			qs = Train.objects.filter(category = oper, number = int(number))
		else:
			qs = Train.objects.filter(number = int(name))

		if variant is None:
			return qs
		else:
			return qs.filter(variant = variant)

	@staticmethod
	def get_trains(start, end, date):
		stops = TrainStop.objects.filter(timetable__date = date).filter(station = start)
		result = []
		for s in stops:
			to_search = [ (s.timetable, s.order) ]
			
			to_search.extend(s.timetable.get_couplings(s.order))

			for tt, order in to_search:
				e = tt.stops().filter(station = end).filter(order__gt = order)
				if e.exists():
					result.append((tt.train, tt, s, e[0]))
		
		return result

	def get_relation_string(self):
		def _(manager):
			return '/'.join(x.get_pretty_name() for x in manager.all())
		return '{} - {}'.format(_(self.source), _(self.destination))
	get_relation_string.short_description = "Relacja pociągu"

	@staticmethod
	def fromHafas(hafas_train):
		raise KolstatError('Called fromHafas')
		op = hafas_train.type
		nu = hafas_train.number
		
		try:
			return Train.objects.get(operator = op, number = nu)
		except Train.DoesNotExist:
			t = Train(operator = op, number = nu)
			t.save()
			t.get_timetable()
			t.update_relation()
			return t
		
	def add_vote(self, delay, clean, composition, user = None):
		a = None
		b = None
		c = None
		if delay != 0:
			a = Vote(type = 'DEL', train = self, note = delay, user = user)
			a.save()
		if clean != 0:
			b = Vote(type = 'CLE', train = self, note = clean, user = user)
			b.save()
		 
		if composition is not None:
			composition.save()
			c =CompositionVote(train = self, composition = composition, user = user)
			c.save()
		return a,b,c
		
	def get_average_delay(self):
		return 6-self.vote_set.filter(type = 'DEL').aggregate(Avg('note'))['note__avg']
	  
	def get_average_clean(self):
		return 6-self.vote_set.filter(type = 'CLE').aggregate(Avg('note'))['note__avg']
		
	def get_compositions(self):
		return self.compositionvote_set.values('composition__composition').annotate(num = Count('composition')).order_by('-num')

	def __str__(self):
		return "{} {} \"{}\"".format(self.category, self.number, self.variant)

	__unicode__ = __str__

	class Meta:
		app_label = 'kolstatapp'
		verbose_name = 'pociąg'
		verbose_name_plural = 'pociągi'
		
class Vote(models.Model):
	def __init__(self, *args, **kwargs):
		super(Vote, self).__init__(*args, **kwargs)
		if 'user' in kwargs:
			self.user = kwargs['user']
		self.date = datetime.now()
		
	train = models.ForeignKey(Train)
	note = models.IntegerField()
	type = models.CharField(max_length = 3, choices = (('DEL', 'Delay'), ('CLE', 'Clean')))
	user = models.ForeignKey(User, null = True)
	date = models.DateTimeField()
	
	class Meta:
		app_label = 'kolstatapp'
		
class CompositionVote(models.Model):
	def __init__(self, *args, **kwargs):
		super(CompositionVote, self).__init__(*args, **kwargs)
		if 'user' in kwargs:
			self.user = kwargs['user']
		self.date = datetime.now()
		
	train = models.ForeignKey(Train)
	composition = models.ForeignKey(Composition)
	user = models.ForeignKey(User, null = True)
	date = models.DateTimeField()
	
	class Meta:
		app_label = 'kolstatapp'
