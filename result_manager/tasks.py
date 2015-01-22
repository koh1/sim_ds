# -*- coding: utf-8 -*-

from celery.task import Task
from celery.decorators import task
from celery.result import AsyncResult
from result_manager.models import ResultSourceMongodb
from result_manager.models import SimulationResult


import os
import sys
import commands
import yaml
import json
import subprocess
import datetime


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

    conf_pst_fix = datetime.datetime.today().strftime("%Y%m%d_%H%M%S")
    fo = open("%s/message_simulator/config_%s.yml" % (os.environ['HOME'], conf_pst_fix,) , "w")
    fo.write(yaml.dump(conf))
    fo.close()

    ## routing configuration
    rt_conf_file = "conf/routing_%d_area%d.csv" % (scale, num_area)

    ## node_spec 
    nd_spec_file = "conf/node_spec_%d.yml" % scale

    ## network definition
    nw_def_file = "conf/network_%d.yml" % scale

    ## area definitiion
    area_def_file = "conf/area_info_%d_area%d.csv" % (scale, num_area)
    
    cdir = "%s/message_simulator" % os.environ['HOME']
    cmd = "python d2xp_sim_system.py config_%s.yml %s %s %s %s" % (conf_pst_fix,
                                                                   rt_conf_file, 
                                                                   nd_spec_file,
                                                                   nw_def_file,
                                                                   area_def_file)

    p = subprocess.Popen(cmd, cwd=cdir, shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    
    ext_code = p.wait()
    result = {}
    result['exit_code'] = ext_code
#    result['stdout'] = p.stdout.readlines()
    result['stdout'] = r"%s" % p.stdout
#    result['stderr'] = p.stderr.readlines()
    result['stderr'] = r"%s" % p.stderr
    logger.info(json.dumps(result, sort_keys=True, indent=2))

    ## very poor implementation because these worker tasks 
    ## are seperated from the simulation program "mbs". 
    ## Simulation ID will be acquired from the log string.
    sim_id = ""
    if ext_code == 0:
        # mbs is successfully completed.
        for line in result['stdout']:
            items = line.split(' ')
            if items[0] == "Simulation":
                sim_id = items[1]
        if sim_id == "":
            ## simulation was failed
            sim_id = "may_be_failed_%s" % datetime.datetime.today().strftime("%Y%m%d%H%M%S")
    
    result['sim_id'] = sim_id
    task_id = exec_d2xp_mbs.request.id

    ## create and issue a task for retrieving the simulation result.
    ## this task will be got by main worker on GUI with MySQL Server
    r = retrieve_mbs_result.apply_async(args=[task_id], queue='MAIN')

    ## store the simulation result. the result will be stored in broker (RabbitMQ)
    return json.dumps(result)

@task
def mbs_exec(conf):
    logger = Task.get_logger()
    return commands.getstatusoutput(cmd)

@task
def exec_mbs():
    logger = Task.get_logger()
    os.chdir("~/message_simulator")
    return os.environ['HOME']

@task
def retrieve_mbs_result(target_task_id):
    r = AsyncResult(target_task_id)
    sr = SimulationResult.objects.get(task_id__exact=target_task_id)
#    sr = SimulationResult.objects.get(sim_id__exact=r['sim_id'])
    result = json.loads(r.result)
    
    if result['exit_code'] == 0:
        ## success
        sr.sim_id = result['sim_id']
        sr.task_progress = 100
        sr.task_status = "SUCCESS"
        sr.save()
    else:
        sr.sim_id = "NO SIM_ID (FAILED)"
        sr.task_status = "FAILED"
        sr.task_progress = 0
        sr.save()

