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

class DiscountAdmin(admin.ModelAdmin):
	list_display = ('kurs90Name', 'description')
	fields = (('kurs90ID', 'kurs90Name'), ('discount', ), ('description', 'documentName'))
admin.site.register(models.Discount, DiscountAdmin)

class UnitClassAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'producer')
	list_filter = ('producer', 'category',)
admin.site.register(models.UnitClass, UnitClassAdmin)

class UnitAdmin(admin.ModelAdmin):
	list_display = ('name', 'evn', 'unitclass', 'producer', 'yearofbuild')
	list_filter = ('unitclass', 'producer', 'yearofbuild')
admin.site.register(models.Unit, UnitAdmin)

def reject_change(modeladm, request, queryset):
	queryset.update(state = 'REJ')
reject_change.short_description = 'Odrzuć bez podania przyczyny'

def accept_change(modeladm, request, queryset):
	for q in queryset:
		q.accept()
accept_change.short_description = 'Zatwierdź bez podania przyczyny'

class UserProfileChangeAdmin(admin.ModelAdmin):
	list_display = ('user', 'field_name', 'current_value', 'new_value', 'state')
	list_filter = ('state', )
	actions = reject_change, accept_change

admin.site.register(models.UserProfileChange, UserProfileChangeAdmin)

class FavPictogramAdmin(admin.ModelAdmin):
	list_display = ('name', )

admin.site.register(models.FavPictogram, FavPictogramAdmin)
