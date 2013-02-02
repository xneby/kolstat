# coding: utf-8
from django import forms

class UserNameChangeForm(forms.Form):
	first_name = forms.CharField(max_length = 100, label = 'Imię')
	last_name = forms.CharField(max_length = 100, label = 'Nazwisko')
