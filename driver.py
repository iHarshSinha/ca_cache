from prettytable import PrettyTable
global q3
q3=[]
global q2
q2=[]
global q4
q4=[]
import math
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
    # print(len(binarybits))
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
            if way.valid_bit == 0:
                way.add_data_for_load(tag, data)
                self.lru_update(way)
                return
        self.evict_during_load(tag, data)
    
    def evict_during_load(self, tag, data):
        max_lru = 0
        evict_way = self.way_list[0]
        for way in self.way_list:
            if way.lru > max_lru:
                max_lru = way.lru
                evict_way = way
        evict_way.evict_data_for_load(tag, data)
        self.lru_update(evict_way)
    
    def miss_during_store(self, tag, data):
        for way in self.way_list:
            if way.valid_bit == 0:
                way.add_data_for_store(tag, data)
                self.lru_update(way)
                return
        self.evict_during_store(tag, data)
    
    def evict_during_store(self, tag, data):
        max_lru = 0
        evict_way = self.way_list[0]
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
        self.sets = []
        self.size = size
        self.block_size = block_size
        self.associativity = associativity
        no_of_set= size//(block_size*associativity)
        self.lines=no_of_set
        self.offset_bits=self.finding_offset_bits()
        self.index_bits=self.finding_index_bits()
        self.tag_bits=self.finding_tag_bits()
        for i in range(no_of_set):
            self.sets.append(Set(associativity))

    def finding_offset_bits(self):
        return int(math.log(self.block_size, 2))
    

    def finding_index_bits(self):
        return int(math.log(self.lines, 2))
    
    def finding_tag_bits(self):
        return int(32 - self.finding_index_bits() - self.finding_offset_bits())


def question1(size,block_size,associativity):
    '''this function will run the cache simulation'''
    '''for each file of input we have a separate cache object'''
    files=['gcc.trace','gzip.trace','mcf.trace','swim.trace','twolf.trace']
    c1 = cache(size,block_size,associativity)
    line_of_instruction1=0
    miss1=0
    return_list=[]
    printer=[[],[],[],[]]
    printer[0]=files

    for f in files:
        c1 = cache(size,block_size,associativity)
        miss1=0
        line_of_instruction1=0

        with open(f, 'r') as file:
            for line in file:
                line_of_instruction1+=1
                line = line.strip()
                parts = line.split()
                l = identifier(parts, c1.index_bits, c1.tag_bits, c1.offset_bits)
                if(l[0]=="Load"):
                    flag=False
                    current_set = c1.sets[int(l[2], 2)]
                    #compare tags of all ways in the set
                    for way in current_set.way_list:
                        if way.tag == l[1]:
                            flag=True
                            current_set.lru_update(way)
                            break
                    if flag==False:
                        miss1+=1
                        current_set.adding_from_memoryu_load(l[1],"data")


                        #evict the data from the first way
                else:
                    flag=False
                    current_set = c1.sets[int(l[2], 2)]
                    #compare tags of all ways in the set
                    for way in current_set.way_list:
                        if way.tag == l[1]:
                            flag=True
                            way.add_data_for_store(l[1], "data")
                            current_set.lru_update(way)
                            break
                    if flag==False:
                        miss1+=1
                        current_set.miss_during_store(l[1],"data")
        printer[1].append(line_of_instruction1)
        printer[2].append((miss1/line_of_instruction1)*100)
        printer[3].append(100-((miss1/line_of_instruction1)*100))
        return_list.append(miss1/line_of_instruction1)
    
    headings=["Files","Total instruction","Miss Rate","Hit rate"]

    
    table=PrettyTable()
    print(f'For 4 way cache with size 1024kb and block size 4')
    transposed_data = list(map(list, zip(*printer)))

    # Create a PrettyTable object
    table = PrettyTable()

    # Set the column headings
    table.field_names = headings

    # Add rows to the table
    for row in transposed_data:
        table.add_row(row)

    # Print the table
    print(table)


    return return_list
    
def question3(size,associativity):
    '''this function will run the cache simulation and will vary the block size from 1 byte to 128 bytes'''
    files=['gcc.trace','gzip.trace','mcf.trace','swim.trace','twolf.trace']
    push_var=0
    printer=[[],[],[],[]]
    printer[0]=files
    return_list=[[] for i in range(0,8) ] 
    block_sizes=[2**i for i in range(0, 8)]
    for block_size in block_sizes:
        printer=[[],[],[],[]]
        printer[0]=files    
        for f in files:
            cache_object = cache(size,block_size,associativity)
            miss=0
            line_of_instruction=0
            with open(f,'r') as file:
                for line in file:
                    line_of_instruction+=1
                    line = line.strip()
                    parts = line.split()
                    l = identifier(parts, cache_object.index_bits, cache_object.tag_bits, cache_object.offset_bits)
                    if(l[0]=="Load"):
                        flag=False
                        current_set = cache_object.sets[int(l[2], 2)]
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
                        current_set = cache_object.sets[int(l[2], 2)]
                        #compare tags of all ways in the set
                        for way in current_set.way_list:
                            if way.tag == l[1]:
                                flag=True
                                way.add_data_for_store(l[1], "data")
                                current_set.lru_update(way)
                                break
                        if flag==False:
                            miss+=1
                            current_set.miss_during_store(l[1],"data")
            printer[1].append(line_of_instruction)
            printer[2].append((miss/line_of_instruction)*100)
            printer[3].append(100-((miss/line_of_instruction)*100))
            return_list[push_var].append((miss/line_of_instruction)*100)
            # print("file done",f)
        push_var+=1
        headings=["Files","Total instruction","Miss Rate","Hit rate"]
        
        table=PrettyTable()
        print(f'For 4 way cache with size 1024kb and block size {block_size}')
        transposed_data = list(map(list, zip(*printer)))

        # Create a PrettyTable object
        table = PrettyTable()

        # Set the column headings
        table.field_names = headings

        # Add rows to the table
        for row in transposed_data:
            table.add_row(row)

        # Print the table
        print(table)
        
        # print("block done",block_size)
    
    # printing tables using prettytables
    main_heading=[f'Block size {2**i}' for i in range(0,8)]
    

    return return_list

            
def question2(block_size,associativity):
    '''this function will run the cache simulation and will vary the cache size from 128kB to 4096 kB'''
    files=['gcc.trace','gzip.trace','mcf.trace','swim.trace','twolf.trace']
    push_var=0
    return_list=[[] for i in range(0,6) ] 
    sizes=[2**i for i in range(7, 13)]
    printer=[[],[],[],[]]
    printer[0]=files
    for size in sizes:
        for f in files:
            cache_object = cache(size*1024,block_size,associativity)
            miss=0
            line_of_instruction=0
            with open(f,'r') as file:
                for line in file:
                    line_of_instruction+=1
                    line = line.strip()
                    parts = line.split()
                    l = identifier(parts, cache_object.index_bits, cache_object.tag_bits, cache_object.offset_bits)
                    if(l[0]=="Load"):
                        flag=False
                        current_set = cache_object.sets[int(l[2], 2)]
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
                        current_set = cache_object.sets[int(l[2], 2)]
                        #compare tags of all ways in the set
                        for way in current_set.way_list:
                            if way.tag == l[1]:
                                flag=True
                                way.add_data_for_store(l[1], "data")
                                current_set.lru_update(way)
                                break
                        if flag==False:
                            miss+=1
                            current_set.miss_during_store(l[1],"data")
            printer[1].append(line_of_instruction)
            printer[2].append((miss/line_of_instruction)*100)
            printer[3].append(100-((miss/line_of_instruction)*100))
            return_list[push_var].append((miss/line_of_instruction)*100)
            # print("file done",f)
        push_var+=1
        headings=["Files","Total instruction","Miss Rate","Hit rate"]
        
        table=PrettyTable()
        print(f'For 4 way cache with size {size} and block size 4')
        transposed_data = list(map(list, zip(*printer)))

        # Create a PrettyTable object
        table = PrettyTable()

        # Set the column headings
        table.field_names = headings

        # Add rows to the table
        for row in transposed_data:
            table.add_row(row)

        # Print the table
        print(table)
        # print("size done",size)
    return return_list   

def question4(size,block_size):
    '''this function will run the cache simulation and will vary the associativity from 1 way to 64 way'''
    files=['gcc.trace','gzip.trace','mcf.trace','swim.trace','twolf.trace']
    push_var=0
    return_list=[[] for i in range(0,7) ] 
    associativities=[2**i for i in range(0, 7)]
    printer=[[],[],[],[]]
    printer[0]=files
    for associativity in associativities:
        for f in files:
            cache_object = cache(size,block_size,associativity)
            miss=0
            line_of_instruction=0
            with open(f,'r') as file:
                for line in file:
                    line_of_instruction+=1
                    line = line.strip()
                    parts = line.split()
                    l = identifier(parts, cache_object.index_bits, cache_object.tag_bits, cache_object.offset_bits)
                    if(l[0]=="Load"):
                        flag=False
                        current_set = cache_object.sets[int(l[2], 2)]
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
                        current_set = cache_object.sets[int(l[2], 2)]
                        #compare tags of all ways in the set
                        for way in current_set.way_list:
                            if way.tag == l[1]:
                                flag=True
                                way.add_data_for_store(l[1], "data")
                                current_set.lru_update(way)
                                break
                        if flag==False:
                            miss+=1
                            current_set.miss_during_store(l[1],"data")
            printer[1].append(line_of_instruction)
            printer[2].append((miss/line_of_instruction)*100)
            printer[3].append(100-((miss/line_of_instruction)*100))
            return_list[push_var].append(100-(miss/line_of_instruction)*100)
            # print("file done",f)
        push_var+=1
        headings=["Files","Total instruction","Miss Rate","Hit rate"]
        
        table=PrettyTable()
        print(f'For {associativity} way cache with size 1024 and block size 4')
        transposed_data = list(map(list, zip(*printer)))

        # Create a PrettyTable object
        table = PrettyTable()

        # Set the column headings
        table.field_names = headings

        # Add rows to the table
        for row in transposed_data:
            table.add_row(row)

        # Print the table
        print(table)
    return return_list


def main():
    # # we can also take input from the user and then create the cache object as our code is dynamic.
    # # '''main function which will create the cache object'''
    global q3
    global q2
    global q4
    print("Question 1 started")
    q1=question1(1024*1024,4,4)
    print("Question 2 started")
    q2=question2(4,4)
    print("Question 3 started")
    q3=question3(1024*1024,4)
    print("Question 4 started")
    q4=question4(1024*1024,4)
    for i in q4:
        print(i)

    

main()

