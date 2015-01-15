from django.db import models

# Create your models here.
class Host(models.Model):
    name = models.CharField(max_length=256)
    ipaddr = models.IPAddressField()
    

    def __unicode__(self):
        return u'%s' % self.name


class Worker(models.Model):
    host = models.ForeignKey(Host)

    login_id = models.CharField(max_length=256)
    login_password = models.CharField(max_length=256)
    ssh_key = models.CharField(max_length=8192)
    
    def __unicode__(self):
        return u'%s' % self.host.name
