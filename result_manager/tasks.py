from celery.task import Task
from celery.decorators import task

import os
import sys
import commands
import yaml


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
def exec_d2xp_mbs(conf, scale, num_area):

    logger = Task.get_logger()
    fo = open("config.yml", "w")
    fo.write(yaml.dump(conf))

    ## routing configuration
    rt_conf_file = "conf/routing_%d_area_%d.csv" % (scale, num_area)

    ## node_spec 
    nd_spec_file = "conf/node_spec_%d.yml" % scale

    ## network definition
    nw_def_file = "conf/network_%d.yml" % scale

    ## area definitiion
    area_def_file = "conf/area_info_%d_area%d.csv"

    os.chdir("/home/vagrant/message_simulator")
    cmd = "python d2xp_system.py config.yml %s %s %s" % (rt_conf_file, 
                                                         nd_spec_file,
                                                         nw_def_file,
                                                         area_def_file)
    return commands.getoutput(cmd)

@task
def mbs_exec(conf):
    logger = Task.get_logger()
    return commands.getstatusoutput(cmd)

@task
def exec_mbs():
    logger = Task.get_logger()
    os.chdir("/home/vagrant/message_simulator")
    return os.environ['HOME']
