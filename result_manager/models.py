from django.db import models

# Create your models here.

class WorkSpace(models.Model):
    pass
    

class ResultSourceMongodb(models.Model):
    host = models.CharField(max_length=512)
    port = models.IntegerField()
    

class SimulationResult(models.Model):
    result_source_mongodb = models.ForeignKey(ResultSourceMongodb)
    db_name = models.CharField(max_length=256)
    sim_id = models.CharField(max_length=256)
    name = models.CharField(max_length=256)


    
