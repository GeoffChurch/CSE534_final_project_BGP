class Node():
    
    def __init__(self, name, scoreFunction):
        self.name = name
        self.scoreFunction = scoreFunction
        self.name2neighbor = dict()
        self.name2bestRouteandScore = {}
        self.inputBuffer = []
        
    def linkTo(self, dst):
        self.name2neighbor[dst.name] = dst
        self.name2bestRouteandScore[dst.name] = {'path': None, 'score': -float('inf')}

    def step(self):
        for path in self.inputBuffer:
            neighborName = path[-1].name
            pathScore = self.scoreFunction(path)
            if name2bestRouteandScore[neighborName]['score'] < pathScore:
                self.name2bestRouteandScore[neighborName]['path'] = path
                self.name2bestRouteandScore[neighborName]['score'] = pathScore
            
                
            
        
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
            node.step()
        for node in nodes:
            node.endStep()
