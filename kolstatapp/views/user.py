# coding: utf-8
from kolstatapp.decorators import expose, login_required
from kolstatapp.exceptions import Redirect
from kolstatapp.models import Journey, Train, UserProfileChange, Discount, FavPictogram, UserFavouriteStation, Station
from kolstatapp.utils.hafas import HafasTrain
from kolstatapp.forms import UserNameChangeForm

from django.contrib import messages
from django.core.urlresolvers import reverse

@login_required
@expose('user/profile.html')
def profile(request):
	name_default = dict(first_name = request.user.first_name,
			last_name = request.user.last_name)

	pending_changes = request.user.userprofilechange_set.order_by('-id')[:5]

	return dict(change_name_form = UserNameChangeForm(initial = name_default), changes = pending_changes)

@login_required
@expose('user/discounts.html')
def discounts(request):
	all_discounts = Discount.objects.order_by('kurs90ID')
	if request.method == 'POST':

		try:
			discounts = Discount.objects.filter(pk__in = (int(x[1:]) for x in request.POST.keys() if x.startswith('d')))
		except ValueError:
			raise Redirect(reverse('user-profile'))
		except Discount.DoesNotExist:
			raise Redirect(reverse('user-profile'))
		
		request.user.get_profile().discounts = discounts

		raise Redirect(reverse('user-profile'))

	user_discounts = request.user.get_profile().discounts.all()

	discounts = ( (d, d in user_discounts) for d in all_discounts)



	return dict(discounts = discounts)

@login_required
@expose('user/favourites.html')
def favourites(request):
	all_picto = FavPictogram.objects.order_by('name')
	were_errors = False

	pictos = []
	for pic in all_picto:
		error = None
		new_station = None
		try:
			current = request.user.get_profile().userfavouritestation_set.get(pictogram = pic).station
		except UserFavouriteStation.DoesNotExist:
			current = None

		if request.method == 'POST':
			if pic.name in request.POST:
				st_name = request.POST[pic.name]
				if st_name:
					try:
						new_station, = Station.search(st_name)
					except ValueError:
						error = 'Brak takiej stacji.'
						were_errors = True

		definition = (pic, current, error, new_station)

		pictos.append(definition)

	if request.method != 'POST' or were_errors:
		return dict(pictos = pictos, errors = were_errors)
	
	current = request.user.get_profile().userfavouritestation_set.all().delete()
	for p, _, _, st in pictos:
		if st is not None:
			UserFavouriteStation.objects.create(profile = request.user.get_profile(), station = st, pictogram = p)
	
	raise Redirect(reverse('user-profile'))

@login_required
@expose('user/change_name.html')
def change_name(request):
	name_default = dict(first_name = request.user.first_name,
			last_name = request.user.last_name)
	
	if request.method == 'POST':
		form = UserNameChangeForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			changed = False

			if data['first_name'] != request.user.first_name:
				changed = True
				UserProfileChange.objects.create( user = request.user, field_name = 'first_name', new_value = data['first_name'] )
			if data['last_name'] != request.user.last_name:
				changed = True
				UserProfileChange.objects.create( user = request.user, field_name = 'last_name', new_value = data['last_name'] )

			if changed:
				messages.success(request,  'Przyjęto żądanie zmiany danych osobowych. Administracja powinna podjąć decyzję bez zbędnej zwłoki.')
			else:
				message.info(request, 'Dane zostały niezmienione')
			
			raise Redirect(reverse('user-profile'))
	else:
		form = UserNameChangeForm(initial = name_default)
	return dict(change_name_form = form)

@login_required
@expose('user/journeys.html')
def journeys(request):

	return dict(journeys = [(j, Train.fromHafas(HafasTrain.fromId(j.trainId))) for j in Journey.objects.filter(user = request.user).order_by('date')])
