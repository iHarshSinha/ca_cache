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
            sets.append(set(associativity))

    def offset_bits(self):
        return math.log(self.block_size, 2)
    

    def index_bits(self):
        return math.log(self.lines, 2)
    
    def tag_bits(self):
        return 32 - self.offset_bits() - self.index_bits()


def runner(main_cache_object):
    pass

def main():
    '''main function which will create the cache object'''
    '''As we have different sizes of cache, block size and associativity, we will take those info from the user'''
    size = int(input("Enter the size of cache in bytes: "))
    block_size = int(input("Enter the block size in bytes: "))
    associativity = int(input("Enter the associativity: "))
    main_cache_object = cache(size, block_size, associativity)
    runner(main_cache_object)

