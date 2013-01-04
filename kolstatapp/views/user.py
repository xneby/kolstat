from kolstatapp.decorators import expose, login_required
from kolstatapp.models import Journey, Train
from kolstatapp.utils.hafas import HafasTrain

@login_required
@expose('user/profile.html')
def profile(request):
	return dict()

@login_required
@expose('user/journeys.html')
def journeys(request):

	return dict(journeys = [(j, Train.fromHafas(HafasTrain.fromId(j.trainId))) for j in Journey.objects.filter(user = request.user).order_by('date')])
