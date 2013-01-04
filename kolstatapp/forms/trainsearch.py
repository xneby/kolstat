# -*- coding: utf-8 -*-
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from datetime import datetime

class TrainSearchForm(forms.Form):
	operator = forms.CharField(required = False)
	number = forms.IntegerField()

