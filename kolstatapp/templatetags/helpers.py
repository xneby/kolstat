from django import template
register = template.Library()
from django.conf import settings
import os.path
from kolstatapp.forms import get_form_by_name
from kolstatapp.utils.forms import underscore_delim
from django.template.loader import select_template
from django.template import Context
from django.core.urlresolvers import reverse

STATIC = settings.STATIC_URL

MAP = {
	'.ico': ('image/x-icon', 'icon', 'img'),
	'.css': ('text/css', 'stylesheet', 'css'),
	'.less': ('text/css', 'stylesheet/less', 'css'),
}

@register.simple_tag
def link(name):
	_, ext = os.path.splitext(name)
	if ext == '.js':
		return '''<script type="text/javascript" src="{root}js/{name}"></script>'''.format(root = STATIC, name = name)
	type, rel, prefix = MAP[ext]
	return '''<link type="{type}" href="{root}{prefix}/{name}" rel="{rel}">'''.format(root = STATIC, name = name, type = type, rel = rel, prefix = prefix)

@register.simple_tag(takes_context = True)
def form(context, form, action, *args):
	if isinstance(form, str):
		form = get_form_by_name(form)()
	if form is None:
		return '###ARG!'

	if action.startswith('rev:'):
		action = reverse(action[4:], args = args)

	template_name = 'forms/' + underscore_delim(form.__class__.__name__) + '.html'

	template = select_template([template_name, 'forms/_default.html'])

	new_context = Context(context)
	new_context.update(dict(form = form, action = action))

	return template.render(context)
