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
    
