from django import template
register = template.Library()
from django.conf import settings
import os.path

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

