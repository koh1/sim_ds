from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from result_manager.models import SimulationResult
from result_manager.models import ResultSourceMongodb
from series_manager.models import DataFrameDef
from main.models import Host

import json
import redis
import logging
import pymongo
import pandas as pd

logger = logging.getLogger('application')
r = redis.Redis(host='127.0.0.1', port=6379, db=10)

def index(request):
    t = loader.get_template('series_manager/index.html')
    dfd = DataFrameDef.objects.all()
    c = RequestContext(request, {
            "data": dfd,
            })
    return HttpResponse(t.render(c))
    

def get_series_with_stats(request):
    pass

def get_series_from_dfd(request):
    dfdid = request.POST['id']
    logger.info(dfdid)
    dfd = DataFrameDef.objects.get(id=dfdid)
    key = "%s_%s" % (dfd.name, request.POST['column_name'])
    value = json.loads(r.get(key))

    ret = {
        "key": key,
        "value": value,
        }
    
    return HttpResponse(json.dumps(ret), content_type='application/json')

def make_df_from_mdb(request):
    series_name = request.POST['series_name']
    sim_id = request.POST['sim_id']
    collection_name = request.POST['collection_name']
    query = json.loads(request.POST['query'])
    column_items = json.loads(request.POST['column_items'])
    dfd = DataFrameDef(
        name = request.POST['series_name'],
        sim_id = request.POST['sim_id'],
        collection_name = request.POST['collection_name'],
        query = request.POST['query'],
        column_items = request.POST['column_items'],
        if_hash = False,
        owner = User.objects.get(id=request.user.id)
        )

    dfd.save()
    result = SimulationResult.objects.filter(sim_id=sim_id)
    if len(result) > 0:
        
        dbinfo = ResultSourceMongodb.objects.get(id=result[0].result_source_mongodb.id)
        dbhost = Host.objects.get(id=dbinfo.host.id)
        db = pymongo.Connection(dbhost.ipaddr, int(dbinfo.port))[result[0].db_name]
        coll = db[collection_name]
        df = pd.DataFrame(list(coll.find(query)))

        for item in column_items:
            json_str = json.dumps(df[item].values.tolist())
            key = "%s_%s" % (series_name, item)
            r.set(key, json_str)

        logger.info("---make_df_from_mdb...OK---")
    
    ret = {
        "status": 0,
        "message": "Data Frame %s is successfully added."  % series_name }

    return HttpResponse(json.dumps(ret), content_type='application/json')
