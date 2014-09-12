from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from result_manager.models import SimulationResult
from result_manager.models import ResultSourceMongodb
from series_manager.models import DataFrameDef
import analyzer.plotter as plotter

import json
import logging
import pymongo
import redis
import pandas as pd


# Create your views here.
r = redis.Redis(host='127.0.0.1', port=6379, db=10)
logger = logging.getLogger('application')

def index(request):
    t = loader.get_template('analyzer/index.html')
    dfds = DataFrameDef.objects.all()
    data = []
    for item in dfds:
        data.append({
                "id": item.id,
                "name": item.name,
                "columns": json.loads(item.column_items),
                })
    c = RequestContext(request, {
            'data': data
            })

    return HttpResponse(t.render(c))

def get_df_sample(request):
    dfd_id = int(request.POST['id'])

    dfd = DataFrameDef.objects.get(id=dfd_id)

    res = {}
    if not dfd == None:

        columns = json.loads(dfd.column_items)

        for col in columns:
            key = "%s_%s" % (dfd.name, col)
            res[col] = json.loads(r.get(key))[-5:-1]
            logger.info(res[col])
            
    return HttpResponse(json.dumps(res), content_type='application/json')

def analyze_index(request, sim_id):
    t = loader.get_template('analyzer/analyze_index.html')
    c = RequestContext(request, {
            "sim_id": sim_id,
            })
    return HttpResponse(t.render(c))
                     
                       
def nwk_index(request, sim_id):
    t = loader.get_template('analyzer/nwk_index.html')
    result = SimulationResult.objects.filter(sim_id=sim_id)
    if len(result) > 0:
        dbinfo = ResultSourceMongodb.objects.get(id=result[0].result_source_mongodb.id)
        db = pymongo.Connection(dbinfo.host, dbinfo.port)[result[0].db_name]

        ## for older version
        confcoll = db['%s_config' % sim_id]
        wnwcoll = db["%s_wide_nwk" % sim_id]
        enwcoll = db["%s_edge_nwk" % sim_id]
        edgendcoll = db["%s_edge" % sim_id]
        msgcoll = db["%s_msg" % sim_id]

        
        c = RequestContext(request, {
                "sim_id": sim_id,
                "conf": list(confcoll.find())[0],
                "nwk_log": list(enwcoll.find().limit(1)),
                "msg_log": list(msgcoll.find().limit(1)),
                "node_log": list(edgendcoll.find().limit(1))
                })
    else:
        c = RequestContext(request, {
                "sim_id": sim_id,
                "conf": {
                    "msg": "No simulation result with sim_id = %s" % sim_id,
                    }
                })

    return HttpResponse(t.render(c))


def get_nwk_chart_img(request):
    sim_id = request.POST['sim_id']
    nwk_name = request.POST['nwk_name']
    result = SimulationResult.objects.filter(sim_id=sim_id)
    if len(result) > 0:
        dbinfo = ResultSourceMongodb.objects.get(id=result[0].result_source_mongodb.id)
        db = pymongo.Connection(dbinfo.host, dbinfo.port)[result[0].db_name]

        ## for older version
        enwcoll = db["%s_edge_nwk" % sim_id]
        df = pd.DataFrame(list(enwcoll.find({"nwk_name": nwk_name})))
        plotter.show_plot(df['time'], df['nw_usage'], "plot.png")
        



def get_nwk_chart_data(request):
    sim_id = request.POST['sim_id']
    nwk_name = request.POST['nwk_name']
    logger.info("%s, %s" % (sim_id, nwk_name))
    result = SimulationResult.objects.filter(sim_id=sim_id)
    ret = []

    if len(result) > 0:
        dbinfo = ResultSourceMongodb.objects.get(id=result[0].result_source_mongodb.id)
        db = pymongo.Connection(dbinfo.host, dbinfo.port)[result[0].db_name]

        ## for older version
        enwcoll = db["%s_edge_nwk" % sim_id]
        
        df = pd.DataFrame(list(enwcoll.find({"nwk_name": nwk_name})))

        ret_x = df[request.POST['x']].values.tolist()
        ret_y = df[request.POST['y']].values.tolist()
        xdata = {'x': ret_x}
        ydata = {'y': ret_y}
        ret.append(xdata)
        ret.append(ydata)
    
    return HttpResponse(json.dumps(ret), content_type='application/json')

