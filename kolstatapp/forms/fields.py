from django import forms
from kolstatapp.models import Station

class StationField(forms.Field):
	def __init__(self, *args, **kwargs):
		if 'widget' not in kwargs:
			kwargs['widget'] = forms.TextInput(attrs = {'class': 'stationField'})
		super(StationField, self).__init__(*args, **kwargs)

	def clean(self, value):
		try:
			st, = Station.search(value)
			return st
		except ValueError:
			raise forms.ValidationError('Brak takiej stacji')
