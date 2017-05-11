from random import random

from graph import Graph

from node import Node


def memoize(f):
    """ Memoization decorator for a function taking a single argument """
    class memodict(dict): 
        def __missing__(self, key):
            ret = self[key] = f(key)
            return ret
    return memodict().__getitem__

        
@memoize
def randomScore(route):
    if route.isDstRepeated():
        return -float('inf')
    return random()#len(route)
        

def local(G, scoreFunction=randomScore):
    # instantiate nodes
    nodes = {name: Node(name=name, scoreFunction=scoreFunction)
             for name in G.getNodes()}
    print('nodes:')
    print(nodes)
    # connect to neighbors
    for srcName, srcNode in nodes.items():
        for dstName in G.getEdges(srcName):
            srcNode.linkTo(nodes[dstName])

    # print('NEIGHBORS:')
    # for node in nodes.values():
    #     print(node)
    #     for neig in node.neighbors:
    #         print('\t', neig)

    print('\nSTART')
    # start running
    for i in range(len(nodes)):
        if not any(node.outputBuffer for node in nodes.values()):
            print('IT CONVERGED!')
            break
        print('step', i)
        print('-'*40)
        for node in nodes.values():
            node.broadcastChanges()
        for node in nodes.values():
            node.updateSelf()
    score = sum(n.curScore() for n in nodes.values()) / len(nodes)
    print("score = ", score)
    return nodes

# g = Graph()
# n = 100
# p = 0.05
# #A = ord('A')
# #ns = ''.join(chr(A+i) for i in range(n))
# ns = list(map(str,range(n)))

# gdict = dict()
# for src in ns:
#     gdict[src] = []
#     for dst in ns:
#         if src != dst and random() < p:
#             gdict[src].append(dst)

"""
gdict = {
    'A' : 'BE',
    'B' : 'AC',
    'C' : 'BDE',
    'D' : 'CE',
    'E' : 'ACDF',
    'F' : 'E'
}
"""

# for n in gdict:
#     g.addNode(n)

# for n1, n2s in gdict.items():
#     for n2 in n2s:
#         g.addEdge(n1, n2)

        
# nodes = local(g)

# print('END STATE!')
# for nodeName, node in nodes.items():
#     print(nodeName)
#     print(node.curState())
#     print()
