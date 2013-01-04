from django.views import defaults

def page_not_found(request):
	return defaults.page_not_found(request, 'errors/404.html')

def server_error(request):
	return defaults.server_error(request, 'errors/500.html')
