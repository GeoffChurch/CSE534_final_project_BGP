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

class Node():
    
    def __init__(self, name, scoreFunction):
        self.name = name
        self.scoreFunction = scoreFunction # [Node] => float
        self.neighbors = []
        self.bestRoute = dict() # bestRoute[X] returns current best route to X
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
                continue
            route.append(self)
            dst = route[0]

            pathScore = self.scoreFunction(tuple(route))

            if dst in self.bestRoute:
                curBestScore = self.scoreFunction(tuple(self.bestRoute[dst]))
            else:
                curBestScore = -float('inf')

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
    return -len(route)
        
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
    for i in range(100):
        if not any(node.outputBuffer for node in nodes.values()):
            break # IT HATH CONVERGED
        print('step',i)
        for nodeName, node in nodes.items():
            print(nodeName)
            print(node.curState())
            print()
        print('-'*40)
        for node in nodes.values():
            node.broadcastChanges()
        for node in nodes.values():
            node.updateSelf()


g = Graph()
gdict = {
    'A' : 'BE',
    'B' : 'AC',
    'C' : 'BDE',
    'D' : 'CE',
    'E' : 'ACD'
}

for n in gdict:
    g.addNode(n)

for n1, n2s in gdict.items():
    for n2 in n2s:
        g.addEdge(n1, n2)

local(g)
