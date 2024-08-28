import math
#ayush part
#takes in 1 bit of hexadecimal bit and convert it to 4 bits of binary
def hextobin(s):
    dic = {
        '0': '0000', '1': '0001', '2': '0010', '3': '0011',
        '4': '0100', '5': '0101', '6': '0110', '7': '0111',
        '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
        'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'
    }
    return dic[s.upper()]


#iterate through hexadecimal bits to give 32 bit of memory address in binary
def binaryreturn(s):
    s = s[2:]
    binarybits=""
    for i in range(len(s)):
        binarybits+=hextobin(s[i])

    return binarybits

#splits the give address into type of memory access and also splits 32bit into tag,index and offset bits
def identifier(parts,indexbit,tagbit,offsetbit):
    l = []
    if parts[0] == 'l':
        l.append("Load")
    else:
        l.append("Store")

    binarybits = binaryreturn(parts[1])
    print(len(binarybits))
    i = 0
    tag = binarybits[i:i+tagbit]
    i += tagbit
    index = binarybits[i:i+indexbit]
    i += indexbit
    offset = binarybits[i:i+offsetbit]
    
    l.append(tag)
    l.append(index)
    l.append(offset)
    
    return l
#nipun part
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
#my part
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

