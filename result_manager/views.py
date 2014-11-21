from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from result_manager.models import SimulationResult
from result_manager.models import ResultSourceMongodb
from result_manager.tasks import exec_d2xp_mbs
from main.models import Host


import json
import logging
import yaml


logger = logging.getLogger('application')

@login_required
def index(request):
    t = loader.get_template('result_manager/index.html')
    entries = SimulationResult.objects.all()
    res_data = []
    for e in entries:
        mdb = ResultSourceMongodb.objects.get(id=e.result_source_mongodb.id)
        mdbhost = Host.objects.get(id=mdb.host.id)
        res = {
            "name": e.name,
            "sim_id": e.sim_id,
            "db_host": mdbhost.name,
            "db_port": mdb.port,
            "db_name": e.db_name,
            "owner": e.user.name
            }
        res_data.append(res)

    c = RequestContext(request, {
            'data': res_data
            })

    return HttpResponse(t.render(c))


def search_results(request):
    search_key = request.POST['search_key']
    res_data = []
    if search_key != "":
        logger.info(request.POST['search_key'])
        entries = SimulationResult.objects.filter(name__icontains=search_key)
        for e in entries:
            mdb = ResultSourceMongodb.objects.get(id=e.result_source_mongodb.id)
            mdbhost = Host.objects.get(id=mdb.host.id)

            res = {
                "name": e.name,
                "sim_id": e.sim_id,
                "db_host": mdbhost.name,
                "db_port": mdb.port,
                "db_name": e.db_name
                }
            res_data.append(res)

        logger.info("%s" % res_data)
#        json_str = serializers.serialize('json', entries)
        json_str = json.dumps(res_data)
        
    else:
        json_str = json.dumps([])

    return HttpResponse(json_str, content_type='application/json')

    
    
@login_required
def exec_index(request):

    t = loader.get_template('result_manager/exec.html')    
    c = RequestContext(request, {
            'conf': 'dummy',
            })
    return HttpResponse(t.render(c))



@login_required
def exec_process(request):
    
    if len(request.FILES) < 1:
        return HttpResponseRedirect('/exec/')
    
    try:
        bconf = yaml.load(request.FILES['bconffile'].read())
    except yaml.YAMLError, exc:
        logger.error("YAMLError", exc)
        return HttpResponseRedirect('/exec/')
    
    sys_scale = request.POST['scale']
    noarea = request.POST['noarea']

    mdb_host_id = -1
    mdb_host = None
    mdb_hosts = Host.objects.filter(name__exact=bconf['store_mongo_db']['host'])
    if len(mdb_hosts) == 0:
        mdb_host = Host(name=bconf['store_mongo_db']['host'],
                        ipaddr=bconf['store_mongo_db']['host'],
                        if_worker = False,
                        if_result_store = True)
        mdb_host.save()
        mdb_host_id = mdb_host.id
    else:
        mdb_host = mdb_hosts[0]
        mdb_host_id = mdb_host.id
        
    mdb_id = 0
    mdb = None
    mdbs = ResultSourceMongodb.objects.filter(host_id__exact=mdb_host_id,
                                              port__exact=bconf['store_mongo_db']['port'])
    if len(mdbs) == 0:
        # add entry
        mdb = ResultSourceMongodb(host=mdb_host,
                                  port=bconf['store_mongo_db']['port'])
        mdb.save()
        mdb_id = mdb.id
    else:
        mdb = mdbs[0]
        mdb_id = mdb.id

    sr = SimulationResult(result_source_mongodb = mdb,
                          db_name = bconf['store_mongo_db']['db'],
                          sim_id = "",
                          name = "",
                          task_id = "",
                          config = json.dumps(bconf),
                          owner = User.objects.get(id=request.user.id))
    sr.save()

    r = exec_d2xp_mbs.delay(bconf, sys_scale, noarea)
    sr.task_id = r.task_id
    sr.save()

    logger.info("[exec_d2xp_mbs] %s" % r.status)
    logger.info("[exec_d2xp_mbs] \t%s" % r.result)

    # layout
    t = loader.get_template('result_manager/exec_result.html')    
    c = RequestContext(request, {
            'task_id': r.task_id,
            'scale': request.POST['scale'],
            'noarea': request.POST['noarea'],
            })
    return HttpResponse(t.render(c))
