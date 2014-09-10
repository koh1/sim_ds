from django.db import models

# Create your models here.

class DataFrameDef(models.Model):
    name = models.ChartField(max_length=256)
    sim_id = models.ChartField(max_length=512)
    collection_name = models.ChartField(max_length=512)
    query = models.ChartField(max_length=512)
    column_items = models.ChartField(max_length=512)
    if_hash = models.BooleanField()
    owner = models.ForeignKey(User)
    
    def get_fields():
        pass


