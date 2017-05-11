from collections import namedtuple, defaultdict
from random import random

from graph import Graph

def memoize(f):
    """ Memoization decorator for a function taking a single argument """
    class memodict(dict): 
        def __missing__(self, key):
            ret = self[key] = f(key)
            return ret
    return memodict().__getitem__

Message = namedtuple('Message', ['target', 'data'])

class Route(list):
    def getSrc(self):
        return self[0]
    def getDst(self):
        return self[-1]
    def isDstRepeated(self):
        return self[-1] in self[:-1]
    def __repr__(self):
        return reversed(self).__repr__()



class Node():
    
    def __init__(self, name, scoreFunction):
        self.name = name
        self.scoreFunction = scoreFunction # [Node] => float
        self.neighbors = []
        self.dst2nxt2curRoute = defaultdict(dict)
        self.dst2bestRoute = dict() # bestRoute[X] returns current best route to X
        self.inputBuffer = []
        self.outputBuffer = []

    def linkTo(self, neighbor):
        self.neighbors.append(neighbor)
        self.outputBuffer.append(Message(target=neighbor, data=[self])) # queue a message to tell them we're neighbors
        #self.name2bestRouteandScore[dst.name] = {'path': None, 'score': -float('inf')}

    def __hash__(self):
        return self.name.__hash__()

    def __repr__(self):
        return self.name
    
    def updateSelf(self):
        for route in self.inputBuffer:
            if self in route:
                routeScore = -float('inf')
            else:
                route.append(self)
                routeScore = self.scoreFunction(tuple(route))

            dst = route[0]
            if dst in self.bestRoute:
                curBestScore = self.scoreFunction(tuple(self.bestRoute[dst]))
            if curBestScore < pathScore: # higher is better
                self.bestRoute[dst] = route
                outputRoute = route
                for neighbor in self.neighbors:
                    self.outputBuffer.append(Message(target=neighbor, data=outputRoute[:]))

        self.inputBuffer = []

    def broadcastChanges(self):
        for message in self.outputBuffer:
            message.target.inputBuffer.append(message.data)
        self.outputBuffer = []

    def curState(self):
        s = ''
        for dst, route in self.bestRoute.items():
            s += '{} => {}\n'.format(dst, route)
        return s

        
@memoize
def randomScore(route):
    if route.isDstRepeated():
        return -float('inf')
    return random()#len(route)
        
def local(G, scoreFunction=randomScore):
    # instantiate nodes
    nodes = {name: Node(name=name, scoreFunction=scoreFunction) for name in G.getNodes()}
    print('nodes:')
    print(nodes)
    # connect to neighbors
    for srcName, srcNode in nodes.items():
        for dstName in G.getEdges(srcName):
            srcNode.linkTo(nodes[dstName])

    print('NEIGHBORS:')
    for node in nodes.values():
        print(node)
        for neig in node.neighbors:
            print('\t', neig)

    print('\nSTART')
    # start running
    for i in range(len(nodes)):
        if not any(node.outputBuffer for node in nodes.values()):
            print('IT CONVERGED!')
            break
        print('step',i)
        print('-'*40)
        for node in nodes.values():
            node.broadcastChanges()
        for node in nodes.values():
            node.updateSelf()
    return nodes

g = Graph()
n = 100
p = 0.05
#A = ord('A')
#ns = ''.join(chr(A+i) for i in range(n))
ns = list(map(str,range(n)))

gdict = dict()
for src in ns:
    gdict[src] = []
    for dst in ns:
        if src != dst and random() < p:
            gdict[src].append(dst)

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

for n in gdict:
    g.addNode(n)

for n1, n2s in gdict.items():
    for n2 in n2s:
        g.addEdge(n1, n2)

        
nodes = local(g)

print('END STATE!')
for nodeName, node in nodes.items():
    print(nodeName)
    print(node.curState())
    print()
