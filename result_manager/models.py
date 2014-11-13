from django.db import models
from main.models import Host
from django.contrib.auth.models import User

# Create your models here.

class ResultSourceMongodb(models.Model):
    host = models.ForeignKey(Host)
    port = models.IntegerField()
    
    def __unicode__(self):
        h = Host.objects.get(id=self.host.id)
        return u'%s:%s' % (h.ipaddr, str(self.port))
    
class SimulationResult(models.Model):
    result_source_mongodb = models.ForeignKey(ResultSourceMongodb)
    db_name = models.CharField(max_length=256)
    sim_id = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    task_id = models.CharField(max_length=36)
    task_status = models.CharField(max_length=16)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s' % self.name
