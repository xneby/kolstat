from django import forms

class AddTrainForm(forms.Form):
	name = forms.CharField()
