from django.db import models

class Composition(models.Model):
    composition = models.CharField(max_length = 250)
    
    def get_composition(self):
        return self.composition.split('+')
    
    def __unicode__(self):
        return u'Composition {}'.format(self.composition)
    
    class Meta:
        app_label = 'kolstatapp'
