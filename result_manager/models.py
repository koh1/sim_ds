from django.db import models
from main.models import Host
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver


import pymongo

# Create your models here.

class ResultSourceMongodb(models.Model):
    host = models.ForeignKey(Host)
    port = models.IntegerField()

    def get_mongo_connection(self):
        conn = pymongo.Connection(self.host.ipaddr, int(self.port))
        return conn

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
    task_progress = models.IntegerField()
    config = models.TextField()
    owner = models.ForeignKey(User)
    description = models.TextField()
    tags = models.TextField()

    def __unicode__(self):
        return u'%s (%s)' % (self.sim_id, self.task_id)


@receiver(pre_delete, sender=SimulationResult)
def simulation_result_pre_delete_signal(sender, instance, **kwargs):
    mdb = instance.result_source_mongodb.get_mongo_connection()[instance.db_name]
    mdb['%s_nwk' % instance.sim_id].drop()
    mdb['%s_node' % instance.sim_id].drop()
    mdb['%s_usr' % instance.sim_id].drop()
    mdb['%s_msg' % instance.sim_id].drop()
    mdb['configs'].remove({"simulation_id":instance.sim_id})
