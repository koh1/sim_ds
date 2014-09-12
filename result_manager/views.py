from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.template import RequestContext, loader
from result_manager.models import SimulationResult
from result_manager.models import ResultSourceMongodb
from main.models import Host

import json
import logging


logger = logging.getLogger('application')

def index(request):
    t = loader.get_template('result_manager/index.html')
    c = RequestContext(request, {
            'data': 10,
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

    
    

