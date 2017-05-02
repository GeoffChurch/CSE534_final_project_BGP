from collections import defaultdict

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
