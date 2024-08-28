import math
class cache():
    '''this class represent cache level 1'''


    def __init__(self, size, block_size, associativity):
        '''initializing the cache with size, block size and associativity'''
        sets = []
        self.size = size
        self.block_size = block_size
        self.associativity = associativity
        no_of_set= size/(block_size*associativity)
        self.lines=no_of_set
        self.offset_bits=self.offset_bits()
        self.index_bits=self.index_bits()
        self.tag_bits=self.tag_bits()
        for i in range(no_of_set):
            sets.append(set())

    def offset_bits(self):
        return math.log(self.block_size, 2)
    

    def index_bits(self):
        return math.log(self.lines, 2)
    
    def tag_bits(self):
        return 32 - self.offset_bits() - self.index_bits()
class set():
    '''this class represent various sets or lines in the cache'''
    def __init__(self):
        self.ways = []
        for i in range(associativity):
            self.ways.append(way())
class way():
    '''this class represent ways which will actually hold the data in the cache'''