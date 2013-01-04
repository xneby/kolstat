from django.db import models
from django.contrib.auth.models import User
from train import CompositionVote, Vote
from station import Station

class Journey(models.Model):
	user = models.ForeignKey(User, null =True)
	source = models.ForeignKey(Station, related_name='source')
	destination = models.ForeignKey(Station, related_name='destination')
	date = models.DateTimeField()
	trainId = models.CharField(max_length = 30)

	composition_vote = models.ForeignKey(CompositionVote, null = True)
	delay_vote = models.ForeignKey(Vote, null = True, related_name='delay_vote')
	clear_vote = models.ForeignKey(Vote, null = True, related_name='clear_vote')

	class Meta:
		app_label = 'kolstatapp'
