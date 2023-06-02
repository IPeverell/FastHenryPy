#!/usr/bin/env python
# coding: utf-8

import numpy as np
import sys

#assert len(sys.argv) == 6

def gen_nodes_2d(h,g,w,d):
    r=0.1
    g_ = g+w
    l  = 0.5 *(np.pi*d-g_)
    
    #calculate nodes one coil
    assert w<g_ and 2*w<l and w<h
    
    nodes = [
        [g_,r*h],
        [g_,0],
        [l,0],
        [l,h],
        [0,h],
        [0,0],
        [-l,0],
        [-l,h],
        [-g_,h],
        [-g_,r*h]
    ]
    #return nodes
    #add extra horixontal nodes to replicate curves in 3d space
    n=20 #number of segments in 
    atbi =[]
    
    for i,[x,y] in enumerate(nodes[:-1]):
        if i%2==1:
            dx = (nodes[i+1][0]-x)/n
            atbi.append([[x+(num)*dx,y] for num in np.arange(1,n)])
    
    atbi = [x for _ in atbi for x in _]
    q = len(atbi)//4
    
    prod = [
            nodes[0:2],atbi[0:q],
            nodes[2:4],atbi[q:2*q],
            nodes[4:6],atbi[2*q:3*q],
            nodes[6:8],atbi[3*q:],
            nodes[8:10]
                 ]
    prod = [x for _ in prod for x in _]
    return prod

def proj2dto3d(nodes,d):
    r =d/2
    return [ [r*np.cos(x/r),r*np.sin(x/r),y] for [x,y] in nodes]


#parameters /mm
h = 5 #height
g = 1 #actual gap between coils
w = 1 #width of coil
d = 5 #diameter of epr tube ie diameter of coil

nodes = gen_nodes_2d(h,g,w,d)
nodes = proj2dto3d(nodes,d)

#nodes
script = "\n".join( [f"N{i+1} x={x} y={y} z={z}" for i, [x,y,z] in enumerate(nodes)] )

#Break up the string
script = script +"\n\n"

#segments
script = script + "\n".join( [f"E{i+1} N{i+1} N{i+2} w=0.038 h=1" for i,[x,y,z] in enumerate(nodes[:-1])] )

script = """
.units mm
.Default sigma=5.80e4 \n
""" + script + """\n
.external N1 N{:}
.freq fmin=10e6 fmax=20e6 ndec=0.05

.end""".format(len(nodes))


with open('test.inp', 'w') as f:
    f.write(script)

