# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from kolstatapp.models import Discount, Station
from django.db.models.signals import post_save

class FavPictogram(models.Model):
	name = models.CharField(max_length = 16)
#	description = models.CharField(max_length = 100)

	def get_img_url(self):
		return '/static/img/picto/{}.png'.format(self.name)

	class Meta:
		app_label = 'kolstatapp'

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	discounts = models.ManyToManyField(Discount)

	def get_favourites(self):
		return [(x.pictogram, x.station) for x in self.userfavouritestation_set.all()]

	class Meta:
		app_label = 'kolstatapp'

class UserFavouriteStation(models.Model):
	pictogram = models.ForeignKey(FavPictogram)
	profile = models.ForeignKey(UserProfile)
	station = models.ForeignKey(Station)

	class Meta:
		app_label = 'kolstatapp'

STATE_CHOICES = (
	('PEN', 'Oczekuje'),
	('ACC', 'Zrealizowano'),
	('REJ', 'Odrzucono'),
)

FIELD_DICT = dict(
	first_name = 'Imię',
	last_name = 'Nazwisko'
		)

class UserProfileChange(models.Model):
	user = models.ForeignKey(User)

	state = models.CharField(max_length = 3, choices = STATE_CHOICES, default = 'PEN')
	field_name = models.CharField(max_length = 16)
	new_value = models.TextField()

	reason = models.TextField(blank = True, null = True)

	class Meta:
		app_label = 'kolstatapp'
		verbose_name = 'propozycja zmiany danych osobowych'
		verbose_name_plural = 'propozycje zmianych danych osobowych'

	def reject(self, reason):
		if self.state != 'PEN':
			raise ValueError('Change must be pending in order to reject')
		self.state = 'REJ'
		self.reason = reason
		self.save()

	def accept(self, reason = ''):
		if self.state != 'PEN':
			raise ValueError('Change must be pending in order to accept')

		self.user.__setattr__(self.field_name, self.new_value)
		self.user.save()

		self.state = 'ACC'
		self.reason = reason
		self.save()

	def current_value(self):
		return self.user.__getattribute__(self.field_name)

	def field_display(self):
		return FIELD_DICT[self.field_name]

	def state_display(self):
		s = self.get_state_display()
		if self.reason:
			s += ' - ' + self.reason
		return s

def create_user_profile(sender, instance, created, **kwars):
	if created:
		try:
			instance.get_profile()
		except UserProfile.DoesNotExist:
			UserProfile.objects.create(user = instance)
		else:
			pass

post_save.connect(create_user_profile, sender = User)
