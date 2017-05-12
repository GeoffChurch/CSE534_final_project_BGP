from random import random

from graph import Graph

from node import Node

import sys
        
def randomScore(route):
    if route.score is None:
        if route.isSrcRepeated():
            score = -float('inf')
        else:
            score = random()#len(route)
        route.score = score
    return route.score
        

def local(G, scoreFunction=randomScore):
    # instantiate nodes
    nodes = {name: Node(name=name, scoreFunction=scoreFunction)
             for name in G.getNodes()}
    # connect to neighbors
    for srcName, srcNode in nodes.items():
        for dstName in G.getEdges(srcName):
            srcNode.linkTo(nodes[dstName])

    # print('NEIGHBORS:')
    # for node in nodes.values():
    #     print(node)
    #     for neig in node.neighbors:
    #         print('\t', neig)

    # start running
    print('\t', end='')
    for i in range(len(nodes)):
        print(i, end=', ')
        sys.stdout.flush()
        if not any(node.outputBuffer for node in nodes.values()):
            #print('\nIT CONVERGED!')
            break
        #print(i, end=', ')
        #print('-'*40)
        for node in nodes.values():
            node.broadcastChanges()
        for node in nodes.values():
            node.updateSelf()
    print()
    # for node in nodes.values():
    #     for rte in node.dst2bestRoute.items():
    #         print(rte)
    return sum(n.curScore() for n in nodes.values()) / len(nodes)
