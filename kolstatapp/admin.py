# coding: utf-8
from django.contrib import admin
from kolstatapp import models
from django import forms

class TrainAdminForm(forms.ModelForm):
	class Meta:
		model = models.Train

	def clean(self):
		cat = self.cleaned_data['category']
		number = self.cleaned_data['number']

		if not models.Train.in_hafas(cat, number):
			raise forms.ValidationError('Brak pociągu w hafasie')

		if len(models.Train.search('{} {}'.format(cat.name, number))) != 0:
			raise forms.ValidationError('Pociąg istnieje w bazie')

		return self.cleaned_data

class TrainAdmin(admin.ModelAdmin):
	form = TrainAdminForm
	list_display = ('__unicode__', 'get_relation_string')
	fields = (('category', 'number'),)
	list_filter = ('category', 'category__type', 'category__operator' )

	def save_model(self, request, obj, form, change):
		if change:
			obj.save()
		else:
			models.Train.add_train('{} {}'.format(obj.category.name, obj.number), template = obj)

	def delete_model(self, request, obj):
		obj.delete_train()

admin.site.register(models.Train, TrainAdmin)

class StationAdmin(admin.ModelAdmin):
	list_display = ('pretty_name', 'name', 'hafasID', 'kurs90ID', 'gskID')
	fields = (('name', 'pretty_name'), ('hafasID', 'kurs90ID', 'gskID'), ('xCoord', 'yCoord'))
admin.site.register(models.Station, StationAdmin)
admin.site.register(models.Journey)

class TrainCategoryAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'type', 'operator', 'full_name')
admin.site.register(models.TrainCategory, TrainCategoryAdmin)

class OperatorAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'website', 'has_description')
admin.site.register(models.Operator, OperatorAdmin)

class TrainNameAdmin(admin.ModelAdmin):
	list_display = ('number', 'name')
	list_filter = ('name',)
admin.site.register(models.TrainName, TrainNameAdmin)

