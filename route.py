

class Route(list):
    def getSrc(self):
        return self[0]

    def getDst(self):
        return self[-1]

    def isDstRepeated(self):
        return self[-1] in self[:-1]

    def __repr__(self):
        return "Route({})".format(list(reversed(self)).__repr__())

    def __hash__(self):
        return tuple(self).__hash__()

    def copy(self):
        return Route(self[:])
