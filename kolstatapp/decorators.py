from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required

from exceptions import PermissionDenied, Redirect, KolstatError
from django.core.urlresolvers import reverse
from utils.hafas import HafasError

WWW_403 = "errors/403.html"
KOLSTAT_ERROR = "errors/kolstat.html"
HAFAS_ERROR = "errors/hafas.html"

def expose(template):
	def decorator(view_func):
		def view(request, *args, **kwargs):
			try:
				context = view_func(request, *args, **kwargs)
				return_code = 200
				render_template = template
			except PermissionDenied as e:
				render_template = WWW_403
				context = {'message': str(e)}
				return_code = 403
#			except KolstatError as e:
#				render_template = KOLSTAT_ERROR
#				context = {'message': str(e)}
#				return_code = 500
			except HafasError as e:
				render_template = HAFAS_ERROR
				context = {'message': str(e)}
				return_code = 500
			except Redirect as e:
				return HttpResponseRedirect(str(e))
			response = render_to_response(render_template, context,
				context_instance = RequestContext(request))
			response.status_code = return_code
			return response
		return view
	return decorator

admin_required = user_passes_test(lambda u: u.is_superuser)
