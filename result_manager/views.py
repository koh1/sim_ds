from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.template import RequestContext, loader
from result_manager.models import SimulationResult
from result_manager.models import ResultSourceMongodb

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
    json_str = ""
    if search_key != "":
        logger.info(request.POST['search_key'])
        entries = SimulationResult.objects.filter(name__icontains=search_key)
#        for e in entries:
#            mdb = ResultSourceMongodb.objects.get(id=e.result_source_mongodb.id)
#            e = mdb.host
#            e.db_port = mdb.port

        json_str = serializers.serialize('json', entries)
        
    else:
        json_str = json.dumps([])

    return HttpResponse(json_str, content_type='application/json')

    
    

