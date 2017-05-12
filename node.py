from collections import namedtuple, defaultdict


from linkedlist import LinkedList

Message = namedtuple('Message', ['target', 'data'])

class Node():
    
    def __init__(self, name, scoreFunction):
        self.name = name
        self.scoreFunction = scoreFunction  # [Node] => float
        self.neighbors = []
        self.dst2nxt2curRoute = defaultdict(dict)
        self.dst2bestRoute = dict() # bestRoute[X] returns current best route to X
        self.inputBuffer = []
        self.outputBuffer = []

    def linkTo(self, neighbor):
        self.neighbors.append(neighbor)
        
        # queue a message to tell them we're neighbors
        self.outputBuffer.append(Message(target=neighbor,
                                         data=LinkedList().append(self)))
        #self.name2bestRouteandScore[dst.name] = {'path': None, 'score': -float('inf')}

    def __hash__(self):
        return self.name.__hash__()

    def __repr__(self):
        return self.name.__repr__()
    
    def updateSelf(self):
        # print("buffer=", self.inputBuffer)
        for rte in self.inputBuffer:
            rte = rte.append(self)
            routeScore = self.scoreFunction(rte)

            dst = rte.getEnd()
            if dst in self.dst2bestRoute:
                curBestScore = self.scoreFunction(self.dst2bestRoute[dst])
            else:
                curBestScore = -float('inf')
            if curBestScore < routeScore: # higher is better
                self.dst2bestRoute[dst] = rte
                for neighbor in self.neighbors:
                    self.outputBuffer.append(Message(target=neighbor,
                                                     data=rte))

        self.inputBuffer = []

    def broadcastChanges(self):
        for message in self.outputBuffer:
            message.target.inputBuffer.append(message.data)
        self.outputBuffer = []

    def curState(self):
        s = ''
        for dst, route in self.dst2bestRoute.items():
            s += '{} => {}\n'.format(dst, route)
        return s

    def curScore(self):
        return sum(self.scoreFunction(p)
                   for p in self.dst2bestRoute.values()) / len(self.dst2bestRoute)
