from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from result_manager.models import SimulationResult
from result_manager.models import ResultSourceMongodb
from series_manager.models import DataFrameDef

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
    

def get_series_with_stats(request):
    logger.info("---get_series_with_stats---")
    sim_id = request.POST['sim_id']
    series_name = request.POST['series_name']
    collection_name = request.POST['collection_name']
    query = json.loads(request.POST['query'])
    column_item = request.POST['column_items']
    proc = request.POST['proc_func']
    result = SimulationResult.objects.filter(sim_id=sim_id)
    
    res = {}
    if len(result) > 0:
        dbinfo = ResultSourceMongodb.objects.get(id=result[0].result_source_mongodb.id)
        db = pymongo.Connection(dbinfo.host, dbinfo.port)[result[0].db_name]

        coll = db[collection_name]
        df = pd.DataFrame(list(coll.find(query)))
        
        if proc == 1: #mean
            df[column_item].mean
        elif proc == 2: #max
            pass
        elif proc == 3: #min
            pass
        elif proc == 4: #std
            pass
        elif proc == 5: #median
            pass
        elif proc == 6: #rolling mean
            pass

def get_series_from_mdb(request):
    logger.info("---get_series_from_mdb---")
    dfd = DataFrameDef(
        name = request.POST['series_name'],
        sim_id = request.POST['sim_id'],
        collection_name = request.POST['collection_name'],
        query = request.POST['query'],
        column_items = request.POST['column_items'],
        if_hash = False,
#        owner = request.user.id
        )
    
    
    sim_id = request.POST['sim_id']
    series_name = request.POST['series_name']
    collection_name = request.POST['collection_name']
    query = json.loads(request.POST['query'])
    column_items = json.loads(request.POST['column_items'])
    result = SimulationResult.objects.filter(sim_id=sim_id)

    ret = {
        'series_name': series_name,
        'series': []
        }


    if len(result) > 0:
        dbinfo = ResultSourceMongodb.objects.get(id=result[0].result_source_mongodb.id)
        db = pymongo.Connection(dbinfo.host, dbinfo.port)[result[0].db_name]

        coll = db[collection_name]
        df = pd.DataFrame(list(coll.find(query)))
        for item in column_items:
            ret['series'].append({
                    item: df[item].values.tolist()
                    })

#        ret['series'] = df.values.tolist()
#        logger.info("%s" % ret)
        
    return HttpResponse(json.dumps(ret), content_type='application/json')
