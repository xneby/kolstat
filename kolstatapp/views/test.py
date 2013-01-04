from kolstatapp.decorators import expose

@expose('test.html')
def test(request):
	return dict()
