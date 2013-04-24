from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required

from .exceptions import PermissionDenied, Redirect, KolstatError, BadRequest
from django.core.urlresolvers import reverse
from .utils.hafas import HafasError
import json

WWW_ERROR = "errors/generic.html"
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
				render_template = WWW_ERROR
				context = {'message': str(e), 'code': 'PermissionDenied'}
				return_code = 403
			except HafasError as e:
				render_template = HAFAS_ERROR
				context = {'message': str(e), 'code': 'HafasError'}
				return_code = 500
			except Redirect as e:
				return HttpResponseRedirect(str(e))
			response = render_to_response(render_template, context,
				context_instance = RequestContext(request))
			response.status_code = return_code
			return response
		return view
	return decorator

def ajax(view_func):
	def view(request, *args, **kwargs):
		try:
			if 'callback' not in request.GET:
				raise BadRequest()
			callback = request.GET['callback']
			data = json.dumps(view_func(request, *args, **kwargs))
			return_code = 200
			render_template = None
		except BadRequest as e:
			render_template = WWW_ERROR
			context = {'message': '', 'code': 'BadRequest'}
			return_code = 400

		if render_template is not None:
			response = render_to_response(render_template, context, context_instance = RequestContext(request))
			response.status_code = return_code
			return response
		else:
			return HttpResponse('{}({})'.format(callback, data), content_type = 'application/json')
	return view

admin_required = user_passes_test(lambda u: u.is_superuser)
