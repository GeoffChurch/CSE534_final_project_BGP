from collections import namedtuple, defaultdict

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

    def updateSelf(self):
        for route in self.inputBuffer:
            dst = route[0]
            pathScore = self.scoreFunction(route)
            curBestScore = self.scoreFunction(self.bestRoute[dst])
            if curBestScore < pathScore: # higher is better
                self.bestRoute[dst] = route
                outputRoute = route + [self]
                for neighbor in self.neighbors:
                    self.outputBuffer.append(Message(target=neighbor, data=outputRoute))
        self.inputBuffer = []

    def broadcastChanges(self):
        for message in self.outputBuffer:
            message.target.inputBuffer.append(message.data)
        self.outputBuffer = []
                
def local(G, scoreFunction):
    # instantiate nodes
    nodes = {name: Node(name=name, scoreFunction=scoreFunction) for name in G.getNodes()}

    # connect to neighbors
    for srcName, srcNode in nodes:
        for dstName in G.getEdges(srcName):
            srcNode.linkTo(nodes[dstName])
    
    # start running
    while True:
        input()
        for node in nodes:
            node.broadcastChanges()
        for node in nodes:
            node.updateSelf()
