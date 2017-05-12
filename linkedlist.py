class LinkedList():

    
    def __init__(self, _head=None, _tail=None):
        # DON'T PLUG IN NONE
        if _tail is None:
            self.head = None
            self.tail = None
            self._len = 0
        else:
            self.head = _head
            self.tail = _tail
            self._len = 1 + len(self.tail)
        self.end = None
        self.score = None

    def isSrcRepeated(self):
        return self.head in self.tail
        
    def getEnd(self):
        if self.end is None:
            cur = self
            while True:
                if cur.tail.tail is None:
                    self.end = (cur.head,)
                    break
                cur = cur.tail
        return self.end[0]

    
    def getHead(self):
        return self.head


    def __repr__(self):
        if len(self) == 0:
            return ''
        return repr(self.head) + ',' + repr(self.tail)
    
    
    def __contains__(self, item):
        if self.head is None and self.tail is None:
            return False
        if item is self.head:
            return True
        return item in self.tail

    
    def append(self, item):
        return LinkedList(_head=item, _tail=self)

    
    def __len__(self):
        return self._len
