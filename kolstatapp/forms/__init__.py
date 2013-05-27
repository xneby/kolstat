from .trainsearch import TrainSearchForm
from .admin import AddTrainForm
from .user import UserNameChangeForm
from .plans import SimpleQueryForm

from kolstatapp.utils.forms import underscore_delim

_forms = [
	'TrainSearchForm',
	'AddTrainForm',
	'UserNameChangeForm',
	'SimpleQueryForm',
]

_form_cache = {}

_functions = [
	lambda x: x,
	underscore_delim
]

for i in _forms:
	form = globals()[i]
	for f in _functions:
		_form_cache[f(i)] = form

def get_form_by_name(name):
	return _form_cache.get(name, None)

__all__ = _forms + ['get_form_by_name']
