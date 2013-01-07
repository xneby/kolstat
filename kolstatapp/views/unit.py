from kolstatapp.decorators import expose
from kolstatapp.models import UnitClass, Unit

#@expose('units/categories.html')
#def units_classes(request)

@expose('units/classes.html')
def units_classes(request):
	category_list = ["EL", "DL", "EMU", "DMU", "C"]
	return dict(classes = [{"name": UnitClass(category=c).get_polish_category_plural(),"classes": [x for x in UnitClass.objects.filter(category = c).order_by('name')]} for c in category_list])

@expose('units/class.html')
def units_class(request, unitclass):
	uc = UnitClass.objects.get(name = unitclass) # mozeby jakos sprawdzac, czy istnienieje, ale nie umiem - szalone przechwytawanie wyjatkow...
	return dict(thisclass = uc, units = Unit.objects.filter(unitclass = uc))
