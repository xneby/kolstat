#!/usr/bin/env python2.7
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'kolstat.settings'

dir = os.path.split(os.path.realpath(__file__))[0]

sys.path.extend([dir + '/../', dir])

import django.core.handlers.wsgi

_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
	environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
	environ['SCRIPT_NAME'] = ''
	return _application(environ, start_response)
