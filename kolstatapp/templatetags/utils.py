from django import template
from django.contrib.auth.forms import AuthenticationForm
register = template.Library()

@register.filter
def timedelta(td):
    s = td.seconds
    H = s // 3600
    s -= H * 3600
    M = s // 60
    s -= M * 60
    
    ret = []
    
    if H > 0: ret.append("{}h".format(H))
    if M > 0: ret.append("{}min".format(M))
    if s > 0: ret.append("{}s".format(s))
    
    if ret == []: return "0s"
    return " ".join(ret)

@register.simple_tag
def percentage(ile, max):
    if ile == '':
        return "NaN"
    return '{:.2f}'.format(ile*100.0/max)

@register.simple_tag
def get_login_form(typ = None):
	form = AuthenticationForm()
	if typ is None:
		return form	
	elif typ == 'as_p':
		return form.as_p()
