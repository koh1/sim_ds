from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from result_manager.models import SimulationResult

import json

def index(request):
    t = loader.get_template('result_manager/index.html')
    c = RequestContext(request, {
            'data': 10,
            })

    return HttpResponse(t.render(c))


def search_results(request):

    entries = SimulationResult.objects.filter(name__icontains=request.POST['key'])
    return HttpResponse(json.dumps(entries), mimetype='application/json')
    
    

