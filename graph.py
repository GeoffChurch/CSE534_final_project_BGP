from collections import defaultdict
import random

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

    for n in range(n):
        g.addNode(n)

    for src in range(n):
        for dst in range(src):
            if random.random() < p:
                g.addEdge(src, dst)

    return g


def randTree(n):
    g = Graph()
    g.addNode(0)
    for i in range(1, n):
        g.addNode(i)
        g.addEdge(i, random.choice(range(i)))
    return g


def randConnectedGraph(n, d):
    """
    constructs a random connected graph on n nodes with exactly floor(n*r) edges
    """
    total_edges = int(n * (n - 1) * d) # floor
    if total_edges < n - 1:
        raise ValueError("A connected graph on {} nodes must have at least {} edges, but with edge density {} would have only {} edges.".format(n, n-1, d, total_edges))
    g = randTree(n)
    choices = [(src, dst) for src in range(n) for dst in range(src) if dst not in g.getEdges(src)]
    random.shuffle(choices) # pretty space inefficient to construct whole list but guaranteed to terminate
    choices = choices[:total_edges - (n - 1)]
    for src, dst in choices:
        g.addEdge(src, dst)
    return g


def randConnectedGraphP(n, p):
    """
    constructs a random connected graph on n nodes where each additional edge has probability p of being included
    """
    g = randTree(n)
    for src in g.getNodes():
        for dst in g.getNodes():
            if src != dst and random.random() < p:
                g.addEdge(src, dst)
                g.addEdge(dst, src)
    return g
        

def createGraph(n, d, func):
    return {
        "rand-graph" : randGraph,
        "rand-connected-graph" : randConnectedGraph,
    }[func](n, d)
