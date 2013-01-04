# coding: utf-8
from kolstatapp.decorators import expose, Redirect, reverse
from kolstatapp.forms import TrainSearchForm
from kolstatapp.models import Train

@expose('train-search.html')
def trainsearch(request):
	if request.method == 'POST':
		form = TrainSearchForm(request.POST)

		if form.is_valid():
			data = form.cleaned_data
			
			query = dict(search_operator = data['operator'] , search_number = data['number'])

			if data['operator']:
				ss = data['operator'] + ' ' + str(data['number'])
			else:
				ss = str(data['number'])
			sr = Train.search(ss)

			if len(sr) == 0:
				query.update(dict(message = 'Brak pociągów w bazie danych spełniających kryteria wyszukiwania'))
				return query
			elif len(sr) > 1:
				query.update(dict(trains = sr))
				return query
			else:
				train, = sr
				
				raise Redirect(reverse('kolstat-train', args=[train.category.name, train.number]))


		else:
			return dict(message = 'Musisz podać numer pociągu')

	return dict()
