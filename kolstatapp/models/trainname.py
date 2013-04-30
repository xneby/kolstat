from django.db import models

class TrainName(models.Model):
	number = models.IntegerField(unique = True)
	category = models.CharField(max_length = 4)
	name = models.CharField(max_length = 100)

	@classmethod
	def getName(cls, train):
		try:
			return cls.objects.get(number = train.number, category = train.category.name).name
		except cls.DoesNotExist:
			return '{}'.format(train.number)

	class Meta:
		app_label = 'kolstatapp'
