from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from result_manager.models import SimulationResult
from result_manager.models import ResultSourceMongodb

import json
import logging
import pymongo
import pandas as pd

logger = logging.getLogger('application')

def index(request):
    t = loader.get_template('series_manager/index.html')
    c = RequestContext(request, {
            "data": 10,
            })
    return HttpResponse(t.render(c))
    
def get_series_from_mdb(request):
    logger.info("---get_series_from_mdb---")
    sim_id = request.POST['sim_id']
    series_name = request.POST['series_name']
    collection_name = request.POST['collection_name']
    query = json.loads(request.POST['query'])
    result = SimulationResult.objects.filter(sim_id=sim_id)

    ret = {
        'series_name': series_name,
        'series': []
        }


    if len(result) > 0:
        dbinfo = ResultSourceMongodb.objects.get(id=result[0].result_source_mongodb.id)
        db = pymongo.Connection(dbinfo.host, dbinfo.port)[result[0].db_name]

        coll = db[collection_name]
        logger.info("collection_name: %s" % collection_name)
        df = pd.DataFrame(list(coll.find(query)))
        del df['_id']
        ret['series'] = df.values.tolist()
        logger.info("%s" % ret)
        
    return HttpResponse(json.dumps(ret), content_type='application/json')
