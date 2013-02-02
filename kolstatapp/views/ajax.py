import json
from kolstatapp.models import Station, UserFavouriteStation as UFS
from kolstatapp.decorators import ajax
from kolstatapp.exceptions import BadRequest

@ajax
def ajax_station(request):
	for field in ('query','type'):
		if field not in request.GET:
			raise BadRequest()

	name = request.GET['query']
	type = request.GET['type']

	if len(name) < 3 and not (name.isdigit() and type == 'kurs90'):
		return []
	
	if type=='name':
		return [st.name for st in Station.objects.filter(name__startswith = name)]
	if type=='kurs90':
		try:
			return [Station.objects.get(kurs90ID = int(name)).name]
		except Station.DoesNotExist:
			return []

	return []

@ajax
def ajax_favourites(request):
	if not request.user.is_authenticated():
		return dict()
	return { pic.name: st.get_pretty_name() for pic, st in request.user.get_profile().get_favourites() }

