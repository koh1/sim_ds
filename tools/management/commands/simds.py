import sys
import json

from pymongo import MongoClient
from django.core.management.base import BaseCommand
from result_manager.models import SimulationResult
from result_manager.models import ResultSourceMongodb
from main.models import Host
from django.contrib.auth.models import User

class Command(BaseCommand):
    args = '<mongodb_host, mongodb_port ...>'

    def get_db_list(self, mc):
        return mc.database_names()

    def get_colls(self, mc, db):
        return mc[db].collection_names()

    def show_sim_configs(self, mc, db):
        return list(mc[db]['configs'].find(limit=1))[0]

    def bulk_register_result(self, mc):
        dbs = mc.database_names()
        hosts = list(Host.objects.filter(ipaddr=mc.host))
        if len(hosts) > 0:
            h = hosts[0]
        else:
            h = Host(
                name = mc.host,
                ipaddr = mc.host
            )
        mdbs = list(ResultSourceMongodb.objects.filter(host = h))
        if len(mdbs) > 0:
            mdb = mdbs[0]
        else:
            mdb = ResultSourceMongodb(
                host = h,
                port = mc.port
            )
        user = list(User.objects.filter(is_superuser=True))[0]
        for db in dbs:
            configs = list(mc[db]['configs'].find())
            if len(configs) < 1:
                continue
            for config in configs:
                del(config["_id"])
                if len(list(SimulationResult.objects.filter(sim_id=config["simulation_id"]))) > 0:
                    continue
                
                sr = SimulationResult(
                    db_name = db,
                    collections = mc[db].collection_names(),
                    sim_id = config["simulation_id"],
                    name = config["simulation_id"],
                    task_id = "",
                    task_status = "",
                    task_progress = 100,
                    config = json.dumps(config),
                    owner = user,
                    result_source_mongodb = mdb,
                    description = "registered afterwards",
                    tags = ""
                )
                sr.save()

    def handle(self, *args, **options):
        mc = MongoClient(args[0], int(args[1]))

        if args[2] == "listdb":
            print(self.get_db_list(mc))
        elif args[2] == "listcoll":
            print(self.get_colls(mc, args[3]))
        elif args[2] == "config":
            print(self.show_sim_configs(mc, args[3]))
        elif args[2] == "regall":
            self.bulk_register_result(mc)
    
if __name__ == '__main__':
    pass

