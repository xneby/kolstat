from kolstatapp.decorators import expose

@expose('home.html')
def home(request):
	return dict()
