from collections import defaultdict
from random import random, choice

class Edge():
    def __init__(self, n1, n2, data=None):
        self.n1 = n1
        self.n2 = n2
        self.data = data

class Graph():
    def __init__(self):
        self.node2data = dict()
        self.node2node2edge = defaultdict(dict)

    def addNode(self, n, data=None):
        self.node2data[n] = data
        
    def addEdge(self, n1, n2, data=None): # undirected
        edge = Edge(n1, n2, data)
        self.node2node2edge[n1][n2] = edge
        self.node2node2edge[n2][n1] = edge

    def getEdge(self, n1, n2):
        return self.node2node2edge[n1][n2]

    def getEdges(self, n1):
        return self.node2node2edge[n1]

    def getData(self, n):
        return self.node2data[n]

    def setData(self, n, data):
        self.node2data[n] = data

    def getNodes(self):
        return list(self.node2data.keys())

        
def randGraph(n, p):
    g = Graph()
    ns = list(map(str,range(n)))
    gdict = dict()
    for src in ns:
        gdict[src] = []
        for dst in ns:
            if src != dst and random() < p:
                gdict[src].append(dst)

    for n in gdict:
        g.addNode(n)

    for n1, n2s in gdict.items():
        for n2 in n2s:
            g.addEdge(n1, n2)

    return g


def randSpanningTree(n):
    g = Graph()
    g.addNode(0)
    for i in range(1, n):
        g.addNode(i)
        g.addEdge(i, choice(range(i)))
    return g


def randConnectedGraph(n, p):
    g = randSpanningTree(n)
    for src in g.getNodes():
        for dst in g.getNodes():
            if random() < p:
                g.addEdge(src, dst)
                g.addEdge(dst, src)
    return g
        

def randDegreeGraph(n, p):
    pass


def createGraph(n, p, func="rand-edge"):
    return {
        "rand-connected-graph" : randConnectedGraph,
        "rand-degree" : randDegreeGraph
    }[func](n, p)
