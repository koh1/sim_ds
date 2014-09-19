from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from result_manager.models import SimulationResult
from result_manager.models import ResultSourceMongodb
from main.models import Host
import analyzer.plotter as plotter


import json
import logging
import pymongo
import pandas as pd

# Create your views here.

logger = logging.getLogger('application')

def index(request, sim_id):
    t = loader.get_template('result_viewer/index.html')
    result = SimulationResult.objects.filter(sim_id=sim_id)
    if len(result) > 0:
        dbinfo = ResultSourceMongodb.objects.get(id=result[0].result_source_mongodb.id)
        dbhost = Host.objects.get(id=dbinfo.host.id)
        db = pymongo.Connection(dbhost.ipaddr, int(dbinfo.port))[result[0].db_name]

        ## for older version
#        confcoll = db['%s_config' % sim_id]
#        wnwcoll = db["%s_wide_nwk" % sim_id]
#        enwcoll = db["%s_edge_nwk" % sim_id]
#        edgendcoll = db["%s_edge" % sim_id]
#        msgcoll = db["%s_msg" % sim_id]

        ## for Newer version
        confcoll = db['configs']
        nwcoll = db["%s_nwk" % sim_id]
        ndcoll = db["%s_node" % sim_id]
        msgcoll = db["%s_msg" % sim_id]
        

        c = RequestContext(request, {
                "sim_id": sim_id,
                "conf": list(confcoll.find({"simulation_id": sim_id}))[0],
                "nwk_log": list(nwcoll.find().limit(1)),
                "msg_log": list(msgcoll.find().limit(1)),
                "node_log": list(ndcoll.find().limit(1))
                })
    else:
        c = RequestContext(request, {
                "sim_id": sim_id,
                "conf": {
                    "msg": "No simulation result with sim_id = %s" % sim_id,
                    }
                })

    return HttpResponse(t.render(c))

def nwk_index(request, sim_id):
    t = loader.get_template('result_viewer/nwk_index.html')
    result = SimulationResult.objects.filter(sim_id=sim_id)
    if len(result) > 0:
        dbinfo = ResultSourceMongodb.objects.get(id=result[0].result_source_mongodb.id)
        db = pymongo.Connection(dbinfo.host, int(dbinfo.port))[result[0].db_name]

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
        dbhost = Host.objects.get(id=dbinfo.host.id)
        db = pymongo.Connection(dbhost, dbinfo.port)[result[0].db_name]

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

def msg_index(request, sim_id):
    t = loader.get_template('result_viewer/msg_index.html')
    return HttpResponse(t.render(c))


def nd_index(request, sim_id):
    t = loader.get_template('result_viewer/nd_index.html')
    return HttpResponse(t.render(c))

