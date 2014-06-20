from django.db import models

# Create your models here.
class SimConfigProto(models.Model):
    sim_id = models.CharField(max_length=512)
    mongo_host = models.CharField(max_length=256)
    mongo_port = models.IntegerField()
    mongo_dbname = models.CharField(max_length=256)
    

    def __unicode__(self):
        return self.sim_id
