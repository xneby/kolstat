from kolstatapp.decorators import expose, admin_required, reverse
from kolstatapp.models import Train
from kolstatapp.exceptions import Redirect
from django.shortcuts import get_object_or_404
from kolstatapp.forms import AddTrainForm

@admin_required
@expose('trains/list.html')
def train_list(request):
	trains = {}
	for t in Train.objects.all():
		if t.category.name not in trains:
			trains[t.category.name] = []
		trains[t.category.name].append(t)

	return dict(trains = [ (k, trains[k]) for k in sorted(trains) ], form = AddTrainForm())

@admin_required
@expose('')
def train_delete(request, train_id):
	train = get_object_or_404(Train, pk = train_id)

	train.delete_train()

	raise Redirect(reverse('admin-trains'))

@admin_required
@expose('trains/add.html')
def train_add(request):
	if request.method == 'POST':
		form = AddTrainForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			
			train = Train.add_train(name)

			raise Redirect(reverse('kolstat-train', args=[train.operator, train.number]))
	else:
		form = AddTrainForm()

	return dict(form = form)

