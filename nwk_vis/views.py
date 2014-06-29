from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

import pymongo
import json

# Create your views here.
def index(request):
    t = loader.get_template('nwk_vis/index.html')
    c = RequestContext(request, {
            'date': 1000,
            })
    return HttpResponse(t.render(c))


def get_nwk_traffic(request, db_name, coll_name, time):
    db = pymongo.Connection('localhost', 27017)[db_name]
    nwk_coll = db[coll_name]
    data = []
    for row in list(nwk_coll.find({"time": int(time)})):
        del row['_id']
        data.append(row)

    return HttpResponse(json.dumps(data), content_type="application/json")


def get_topology_data(request, db_name, coll_name):
    db = pymongo.Connection('localhost', 27017)[db_name]
    topo_coll = db[coll_name]
    data = list(topo_coll.find())[0]
    
    
