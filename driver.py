import math
miss=0
line_of_instruction = 0
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
        self.valid_bit = 0
        self.dirty_bit = 0
        self.tag = ""
        self.data = ""
        self.lru = 0

    def add_data_for_store(self, tag, data):
        self.valid_bit = 1
        self.dirty_bit = 1
        self.tag = tag
        self.data = data
        self.lru = 0
    
    def add_data_for_load(self, tag, data):
        self.valid_bit = 1
        self.dirty_bit = 0
        self.tag = tag
        self.data = data
        self.lru = 0
    
    def evict_data_for_load(self, new_tag, new_data):
        if self.dirty_bit:
            self.dirty_bit = 0
        self.tag = ""
        self.data = ""
        self.add_data_for_load(new_tag, new_data)

    def evict_data_for_store(self, new_tag, new_data):
        if self.dirty_bit:
            self.dirty_bit = 0
        self.tag = ""
        self.data = ""
        self.add_data_for_store(new_tag, new_data)


class Set:
    '''this class represent various sets or lines in the cache'''

    def __init__(self, ways):
        self.way = ways
        self.way_list = []  #list for way object
        for i in range(ways):
            self.way_list.append(Way())

    
    def lru_update(self,hit_way):
        for way in self.way_list:
            way.lru += 1
        hit_way.lru = 0 
    
    def adding_from_memoryu_load(self,tag,data):
        for way in self.way_list:
            if way.tag == "":
                way.add_data_for_load(tag, data)
                self.lru_update(way)
                return
        self.evict(tag, data)
    
    def evict(self, tag, data):
        max_lru = 0
        evict_way = None
        for way in self.way_list:
            if way.lru > max_lru:
                max_lru = way.lru
                evict_way = way
        evict_way.add_data_for_load(tag, data)
        self.lru_update(evict_way)
    
    def miss_during_store(self, tag, data):
        for way in self.way_list:
            if way.tag == "":
                way.add_data_for_store(tag, data)
                self.lru_update(way)
                return
        self.evict_during_store(tag, data)
    
    def evict_during_store(self, tag, data):
        max_lru = 0
        evict_way = None
        for way in self.way_list:
            if way.lru > max_lru:
                max_lru = way.lru
                evict_way = way
        evict_way.evict_data_for_store(tag, data)
        self.lru_update(evict_way)




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
    global line_of_instruction
    global miss
    with open('gcc.trace', 'r') as file:
        for line in file:
            line_of_instruction+=1
            line = line.strip()
            parts = line.split()
            l = identifier(parts, main_cache_object.index_bits, main_cache_object.tag_bits, main_cache_object.offset_bits)
            if(l[0]=="Load"):
                flag=False
                current_set = main_cache_object.sets[int(l[2], 2)]
                #compare tags of all ways in the set
                for way in current_set.way_list:
                    if way.tag == l[1]:
                        flag=True
                        current_set.lru_update(way)
                        break
                if flag==False:
                    miss+=1
                    current_set.adding_from_memoryu_load(l[1],"data")


                    #evict the data from the first way
            else:
                flag=False
                current_set = main_cache_object.sets[int(l[2], 2)]
                #compare tags of all ways in the set
                for way in current_set.way_list:
                    if way.tag == l[1]:
                        flag=True
                        way.add_data_for_store(l[1], "data");
                        current_set.lru_update(way)
                        break
                if flag==False:
                    miss+=1
                    current_set.miss_during_store(l[1],"data")

    

def main():
    '''main function which will create the cache object'''
    '''As we have different sizes of cache, block size and associativity, we will take those info from the user'''
    size = int(input("Enter the size of cache in bytes: "))
    block_size = int(input("Enter the block size in bytes: "))
    associativity = int(input("Enter the associativity: "))
    main_cache_object = cache(size, block_size, associativity)
    runner(main_cache_object)

