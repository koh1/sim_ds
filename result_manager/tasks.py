from celery.task import Task
from celery.decorators import task

import os
import sys

class AddTask(Task):
    def rung(self, x, y):
        logger = self.get_logger(task_name=u'class')
        logger.info("Adding %s + %s" % (x, y))
        return x + y

@task
def add(x, y):
    logger = Task.get_logger(task_name=u'decorator')
    logger.info("Adding %s + %s" % (x, y))
    return x + y

@task
def exec_d2xp_mbs(conf, route, nd_spec, nw_def, area_def):
    logger = Task.get_logger()
    
@task
def exec_mbs():
    logger = Task.get_logger()
    os.chdir("/home/vagrant/message_simulator")
    return os.environ['HOME']
