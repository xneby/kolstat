# coding: utf-8
from django import forms
from fields import StationField
from datetime import date

class SimpleQueryForm(forms.Form):
	start = StationField(label='Stacja początkowa')
	end = StationField(label='Stacja końcowa')
	date = forms.DateField(label='Data wyjazdu', initial = date.today)
	time = forms.TimeField(label='Godzina wyjazdu')
