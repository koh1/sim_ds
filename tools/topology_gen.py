
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


    
