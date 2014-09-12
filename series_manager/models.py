from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class DataFrameDef(models.Model):
    name = models.CharField(max_length=256)
    sim_id = models.CharField(max_length=512)
    collection_name = models.CharField(max_length=512)
    query = models.CharField(max_length=512)
    column_items = models.CharField(max_length=512)
    if_hash = models.BooleanField()
    owner = models.ForeignKey(User)
    
    def get_fields():
        pass


    def __unicode__(self):
        return u'%s' % self.name
