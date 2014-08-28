from django.contrib import admin
from result_manager.models import ResultSourceMongodb
from result_manager.models import SimulationResult
# Register your models here.


admin.site.register(ResultSourceMongodb)
admin.site.register(SimulationResult)
