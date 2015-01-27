

def convert_for_d3(data):
    root = "SW-L1-1-1"
    tree = {"name": root,
            "children": []}
    convert_hash_for_d3_make_children(tree["children"], root, data)
    return tree

def convert_for_d3_make_children(parent, p_name, data):
    for c in data[p_name]["children"]:
        cobj = {"name": c, "children": []}
        convert_for_d3_make_children(cobj["children"], c, data)
        parent.append(cobj)
def convert_hash_for_d3_make_children(parent, p_name, data):
    for k,v in data[p_name]["children"].items():
        print "node: %s" % k
        cobj = {"name": k, "children": []}
        convert_hash_for_d3_make_children(cobj["children"], k, data)
        parent.append(cobj)

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
    topology[entry["name"]]["children"] = {}
def get_topology_data_proto(csv_data):
    import numpy as np

    topology = {}
    for row in csv_data:
        src = get_component_object(row[0])
        if not topology.has_key(src["name"]):
            add_topology_entry(topology, src)

        dst = get_component_object(row[1])
        if not topology.has_key(dst["name"]):
            add_topology_entry(topology, dst)

        if len(row) == 2:
            v = which_is_parent(src, dst)
            if v == 0:
                topology[src["name"]]["children"][dst["name"]] = 1
            elif v == 1:
                topology[dst["name"]]["children"][src["name"]] = 1
            else:
                print("could not judge which is parent.")
                sys.exit(1)
        elif len(row) == 3:
            mid = get_component_object(row[2])
            if not topology.has_key(mid["name"]):
                add_topology_entry(topology, mid)
            v = which_is_parent(src, mid)
            if v == 0:
                topology[src["name"]]["children"][mid["name"]] = 1
            elif v== 1:
                topology[mid["name"]]["children"][src["name"]] = 1

            v = which_is_parent(mid, dst)
            if v == 0:
                topology[mid["name"]]["children"][dst["name"]] = 1
            elif v == 1:
                topology[dst["name"]]["children"][mid["name"]] = 1
            else:
                print("could not judge which is parent.")
                sys.exit(1)
        else:
            prev_via = src
            via = None
            for i in np.arange(len(row) - 3) + 2:
                via = get_component_object(row[i])
                if topology.has_key(via["name"]):
                    add_topology_entry(topology, via)
                
                v = which_is_parent(prev_via, via)
                if v == 0:
                    topology[prev_via["name"]]["children"][via["name"]] = 1
                elif v == 1:
                    topology[via["name"]]["children"][prev_via["name"]] = 1
                else:
                    print("could not judge which is parent.")
                    sys.exit(1)
                
                prev_via = via
            
            row_tail = get_component_object(row[-1])
            if topology.has_key(row_tail["name"]):
                add_topology_entry(topology, row_tail)
            v = which_is_parent(row_tail, dst)
            if v == 0:
                topology[row_tail["name"]]["children"][dst["name"]] = 1
            elif v == 1:
                topology[dst["name"]]["children"][row_tail["name"]] = 1
            else:
                print("could not judge which is parent.")
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
        obj["level"] = split_name[1][-1]
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
    f_hash.write(json.dumps(topo_hash))
    f_hash.close()
    res = convert_for_d3(topo_hash)
    print("%d entries" % len(res))
    f = open("outout.json", 'w')
    f.write(json.dumps(res))
    f.close()


    
