from django.db import models

# Create your models here.
class Host(models.Model):
    name = models.CharField(max_length=256)
    ipaddr = models.IPAddressField()
    if_worker = models.BooleanField()
    if_result_store = models.BooleanField()
    
    def __unicode__(self):
        return u'%s' % self.name
