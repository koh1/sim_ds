import time
import logging

#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def convert_for_d3(data):
    root = "SW-L0-1-1"
    r = convert_hash_for_d3_make_children(root, data)
    ret = {"name": root,
           "type": data[root]["type"],
           "level": data[root]["level"],
           "children": r}
    return ret

def convert_for_d3_make_children(p_name, data):
    ret = []
    for c in data[p_name]["children"]:
        cobj = {"name": c, "children": r}
        r = convert_for_d3_make_children(c, data)
        ret.append({"name": c,
                    "children": r})
    return ret

def convert_hash_for_d3_make_children(p_name, data):
    ret = []
    for k,v in data[p_name]["children"].items():
        logger.debug("node: %s, %s" % (k,v))
        r = convert_hash_for_d3_make_children(k, data)
        ret.append({"name": k,
                    "type": data[k]["type"],
                    "level": data[k]["level"],
                    "children": r})
    return ret

def which_is_parent(o1, o2):
    if o1["type"] > o2["type"]:
        return 0
    elif o1["type"] < o2["type"]:
        return 1
    else:
        if o1["level"] > o2["level"]:
            return 1
        elif o1["level"] < o2["level"]:
            return 0
        else:
            # error
            return -1 

def add_topology_entry(topology, entry):
    topology[entry["name"]] = {}
    topology[entry["name"]]["name"] = entry["name"]
    topology[entry["name"]]["level"] = entry["level"]
    topology[entry["name"]]["type"] = entry["type"]
    topology[entry["name"]]["children"] = {}

def make_topology_entry(entry):
    logger.debug("COMP[%s] is created" % entry["name"])
    eobj = {}
    eobj["name"] = entry["name"]
    eobj["level"] = entry["level"]
    eobj["type"] = entry["type"]
    eobj["children"] = {}
    return eobj

def get_topology_data_proto(csv_data):
    import numpy as np

    topology = {}
    for row in csv_data:
#        time.sleep(0.1)
        logger.debug(row)
        logger.debug("\ttopology length: %d" % len(topology))
        src = get_component_object(row[0])
        if not topology.has_key(src["name"]):
            topology[src["name"]] = make_topology_entry(src)

        dst = get_component_object(row[1])
        if not topology.has_key(dst["name"]):
            topology[dst["name"]] = make_topology_entry(dst)

        if len(row) == 2:
            logger.debug("\troute length: %d" % len(row))
            v = which_is_parent(src, dst)
            logger.debug("\tcomparing %s and %s" % (src["name"], dst["name"]))
            if v == 0:
                logger.debug("\t%s is parent" % src["name"])
                topology[src["name"]]["children"][dst["name"]] = 1
            elif v == 1:
                logger.debug("\t%s is parent" % dst["name"])
                topology[dst["name"]]["children"][src["name"]] = 1
            else:
                logger.debug("\tcould not judge which is parent.")
                sys.exit(1)

        elif len(row) == 3:
            logger.debug("\troute length: %d" % len(row))
            mid = get_component_object(row[2])
            if not topology.has_key(mid["name"]):
                topology[mid["name"]] = make_topology_entry(mid)

            v = which_is_parent(src, mid)
            logger.debug("\tcomparing %s and %s" % (src["name"], mid["name"]))
            if v == 0:
                logger.debug("\t%s is parent" % src["name"])
                topology[src["name"]]["children"][mid["name"]] = 1
            elif v== 1:
                logger.debug("\t%s is parent" % mid["name"])
                topology[mid["name"]]["children"][src["name"]] = 1
            else:
                logger.debug("\tcould not judge which is parent.")
                sys.exit(1)

            v = which_is_parent(mid, dst)
            logger.debug("\tcomparing %s and %s" % (mid["name"], src["name"]))
            if v == 0:
                logger.debug("\t%s is parent" % mid["name"])
                topology[mid["name"]]["children"][dst["name"]] = 1
            elif v == 1:
                logger.debug("\t%s is parent" % dst["name"])
                topology[dst["name"]]["children"][mid["name"]] = 1
            else:
                logger.debug("\tcould not judge which is parent.")
                sys.exit(1)
        else:
            logger.debug("\troute length: %d" % len(row))
            prev_via = src
            via = None
            for i in np.arange(len(row) - 3) + 2:
                via = get_component_object(row[i])
                if not topology.has_key(via["name"]):
                    topology[via["name"]] = make_topology_entry(via)
                
                v = which_is_parent(prev_via, via)
                logger.debug("\tcomparing %s and %s" % (prev_via["name"], via["name"]))
                if v == 0:
                    logger.debug("\t%s is parent" % prev_via["name"])
                    topology[prev_via["name"]]["children"][via["name"]] = 1
                elif v == 1:
                    logger.debug("\t%s is parent" % via["name"])
                    topology[via["name"]]["children"][prev_via["name"]] = 1
                else:
                    logger.debug("\tcould not judge which is parent.")
                    sys.exit(1)
                
                prev_via = via
            
            row_tail = get_component_object(row[-1])
            if not topology.has_key(row_tail["name"]):
                topology[row_tail["name"]] = make_topology_entry(row_tail)
            v = which_is_parent(row_tail, dst)
            logger.debug("\tcomparing %s and %s" % (row_tail["name"], dst["name"]))
            if v == 0:
                logger.debug("\t%s is parent" % row_tail["name"])
                topology[row_tail["name"]]["children"][dst["name"]] = 1
            elif v == 1:
                logger.debug("\t%s is parent" % dst["name"])
                topology[dst["name"]]["children"][row_tail["name"]] = 1
            else:
                logger.debug("\tcould not judge which is parent.")
                sys.exit(1)
        
    return topology

def get_component_object(component_name):
    obj = {}
    obj["name"] = component_name
    if obj["name"] == "CL":
        obj["level"] = 100
        obj["type"] = 0

    else:
        split_name = component_name.split('-')
        obj["level"] = int(split_name[1][-1])
        if split_name[0] == "SW":
            obj["type"] = 1
        else:
            obj["type"] = 0

    return obj
    

if __name__ == '__main__':
    import json
    import sys
    import csv

    p = sys.argv
    if len(p) < 2:
        print "usage: python %s <original topology.json file>" % p[0]
        sys.exit(0)
    
    
#    topo_org = json.loads(open(p[1]).read())
    routing_csv = csv.reader(open(p[1]), delimiter=',')
    topo_hash = get_topology_data_proto(routing_csv)
    f_hash = open("output_raw.json", 'w')
    f_hash.write(json.dumps(topo_hash, sort_keys=True, indent=2))
    f_hash.close()
    res = convert_for_d3(topo_hash)
    print("%d entries" % len(res))
    f = open("output.json", 'w')
    f.write(json.dumps(res, sort_keys=True, indent=2))
    f.close()


    
