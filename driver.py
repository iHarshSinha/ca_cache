class Way:
    '''this class represent ways which will actually hold the data in the cache'''

    def __init__(self):
        self.dirty_bit = 0
        self.tag = ""
        self.data = ""

    def add_data(self, tag, data):
        self.dirty_bit = 1
        self.tag = tag
        self.data = data

    def evict_data(self, new_tag, new_data):
        if self.dirty_bit:
            self.dirty_bit = 0
            self.tag = ""
            self.data = ""
            self.add_data(new_tag, new_data)


class Set:
    '''this class represent various sets or lines in the cache'''

    def __init__(self, ways):
        self.way = ways
        self.way_list = []  #list for way object

    def add_ways(self):
        i = 0
        while i < self.way:  #initializing a list of ways for a particular set
            way_obj = Way()
            self.way_list.append(way_obj)
            i=i+1


class Cache:
    '''this class represent cache level 1'''
    pass
