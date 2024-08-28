class way():
    '''this class represent ways which will actually hold the data in the cache'''

    def __init__(self, tag, data):
        self.tag = tag
        self.data = data
        self.dirty_bit = 0


class set():
    '''this class represent various sets or lines in the cache'''

    def __init__(self, ways):
        self.way = ways
        self.list = []

    def addways(self):
        i = 0
        while i < self.way:     #initializing a list of ways for a particular set
            way_obj = way(tag,data)
            self.list.append(way_obj)


class cache():
    '''this class represent cache level 1'''
    pass
