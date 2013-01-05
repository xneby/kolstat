from kolstatapp.decorators import expose
from kolstatapp.models import UnitClass

#@expose('units/categories.html')
#def units_classes(request)

@expose('units/classes.html')
def units_classes(request):
	return dict(classes = [x for x in UnitClass.objects.order_by('name')])
