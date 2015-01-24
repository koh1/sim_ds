

def convert_for_d3(data):
    root = "SW-L0-1-1"
    tree = {"name": root,
            "children": []}
    convert_for_d3_make_children(tree["children"], root, data)
    return tree

def convert_for_d3_make_children(parent, p_name, data):
    for c in data[p_name]["children"]:
        cobj = {"name": c, "children": []}
        convert_for_d3_make_children(cobj["children"], c, data)
        parent.append(cobj)


def which_is_parent(o1, o2):
    pass

def get_topology_data_proto(csv_data):
    import numpy as np

    topology = {}
    for row in routes:
        src = get_component_object(row[0])
        if topology[src["name"]] = None:
            topology[src["name"]] = {}
            topology[src["name"]]["name"] = src["name"]
            topology[src["name"]]["level"] = src["level"]
            topology[src["name"]]["children"] = {}

        dst = get_component_object(row[1])
        if topology[dst["name"]] = None:
            topology[dst["name"]] = {}
            topology[dst["name"]]["name"] = src["name"]
            topology[dst["name"]]["level"] = src["level"]
            topology[dst["name"]]["children"] = {}

        if len(row) == 2:
            if src["type"] > dst["type"]:
                topology[src["name"]]["children"][dst["name"]] = 1
            else:
                topology[dst["name"]]["children"][src["name"]] = 1
        elif len(row) == 3:
            pass
        else:
            prev_via = src
            via = None
            for i in np.arange(len(row) - 3) + 2:
                via = get_component_object(row[i])
                if topology[via["name"]] = None:
                    topology[via["name"]] = {}
                    topology[via["name"]]["name"] = via["name"]
                    topology[via["name"]]["level"] = via["level"]
                    topology[via["name"]]["children"] = {}
                
                if prev_via["type"] > via["type"]:
                    topology[prev_via["name"]]["children"][via["name"]] = 1
                else:
                    topology[via["name"]]["children"][prev_via["name"]] = 1
                
                prev_via = via
            
            row_tail = get_component_object(row[-1])
            if topology[row_tail["name"]] = None:
                topology[row_tail["name"]] = {}
                topology[row_tail["name"]]["name"] = row_tail["name"]
                topology[row_tail["name"]]["level"] = row_tail["level"]
                topology[row_tail["name"]]["children"] = {}
            if row_tail["type"] > dst["type"]:
                topology[row_tail["name"]]["children"][dst["name"]] = 1
            else:
                topology[dst["name"]]["children"][row_tail["name"]] = 1
                
        each_route = {}
        each_route['src'] = {
            "name": row[0],
            "type": row[0].split('-')[0],
            "level": int(row[0].split('-')[1][-1])
            }
        each_route['dst'] = {
            "name": row[1],
            "type": row[1].split('-')[0],
            "level": int(row[1].split('-')[1][-1])
            }
        
        if len(row) > 2:
            via = row[2:-1]
            
        else:
            pass


    
def get_component_object(component_name):
    obj = {}
    obj["name"] = component_name
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

    p = sys.argv
    if len(p) < 2:
        print "usage: python %s <original topology.json file>" % p[0]
        sys.exit(0)
    
    
    topo_org = json.loads(open(p[1]).read())
    res = convert_for_d3(topo_org)
    
    f = open("outout.json", 'w')
    f.write(json.dumps(res))
    f.close()


    
