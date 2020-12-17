'''
MPCS 51042 S'20: Markov models and hash tables

M. Merritt Smith
'''
from map import Map
from functools import reduce

class Hashtable(Map):
    """
    class Hashtable(Map):

    A class that implements a hash table in Python. Inherits from the Map 
    abstract base class, implementing the functions laid out there.
    Can store key, value pairs much like a Python dictionary but stores
    them using a hash function as a list of tuples.
    """
    def __init__(self, capacity, defVal, loadfactor, growthFactor):
        """
        __init__(self, capacity, defVal, loadfactor, growthFactor)
        The initialization method for the Hashtable class. 
        Takes in a capacity, the initial max length for the table,
        defVal, the default value for empty locations in the table,
        loadfactor, a float that determines how much of the table should be
        taken up before we expand it, and growthFactor, an int that determines
        how much we should expand the capacity by when we do expand it.
        Defines a _prime_multiplier that is used by _hash, and the central
        table object.

        Gets:
            self, a Hashtable instance
            capacity, an int
            defVal, could be any dtype but typically None
            loadfactor, a float 0 < loadfactor <= 1
            growthFactor, an int > 1
        Returns: nothing explicitly, but self implicitly
        """
        self.capacity = capacity
        self.defVal = defVal
        self.loadfactor = loadfactor
        self.growthFactor = growthFactor
        self._prime_multiplier = 37
        self.table = [defVal]*self.capacity
        self.rehashing = False


    def _hash(self, key):
        """
        _hash(self, key)
        Takes in a key and turns it into a hashed int using Horner's method. 
        Meant to be an internal method.

        Gets: 
            self, a Hashtable instance
            key, a string
        Returns: the hash value, an int
        """
        total = reduce(lambda hash_code, c: (hash_code*self._prime_multiplier + ord(c))%self.capacity, key, 0)
        return total


    def _rehash(self):
        """
        _rehash(self)
        Called if the table goes over its allotted load. Expands the table by the growthFactor,
        filters the data in the table to only the real values (no defaults or deleted vals), 
        expands the table based on the new capacity, then adds all the real values into the 
        new table. Meant to be an internal method.

        Gets: self, a Hashtable instance
        Returns: Nothing
        """
        self.rehashing = True
        self.capacity *= self.growthFactor
        filtered_table = list(filter(lambda x: isinstance(x, tuple) and x[2], self.table))
        self.table = [self.defVal]*self.capacity
        for key_val in filtered_table:
            self.__setitem__(key_val[0], key_val[1])
        self.rehashing = False


    def __getitem__(self, key):
        """
        ___getitem__(self, key)
        A method of the Hashtable class that retrieves and returns the element from the
        table with the provided key. First checks whether the initially computed hash
        value gives a match, and if so returns that immediately. If not found, checks
        through the rest of the table using linear probing until an empty space is found.
        If an empty space is found, break and return the default. If a match is found this way, 
        return it like normal.

        Gets:
            self, a Hashtable instance
            key, a string
        Returns: whatever the key is or the default value is
        """
        hash_val = self._hash(key)
        if self.table[hash_val] != self.defVal and (isinstance(self.table[hash_val], tuple) and 
                                                    self.table[hash_val][0] == key and
                                                    self.table[hash_val][2] == True):
            return self.table[hash_val][1]
        else:
            key_found = False
            iter_count = 0
            while not key_found:
                if hash_val >= self.capacity:
                    hash_val = 0
                if self.table[hash_val] == self.defVal:
                	break
                if self.table[hash_val][0] == key:
                    if self.table[hash_val][2] == True:
                        return self.table[hash_val][1]
                hash_val += 1
                iter_count += 1
        return self.defVal


    def __setitem__(self, key, value):
        """
        __setitem__(self, key, value)
        A method of the Hashtable class that writes new elements to the Hashtable or overwrites
        the element with the provided key. First checks whether the table is currently overloaded,
        and rehashes if so. Then checks whether the initially computed hash value for the key is 
        a tuple with a matching key or the default value or a deleted tuple. If so, writes over 
        that element. If not, checks for a location where the provided key, value pair can be 
        written using linear probing. If a location is not found after a circuit of the table,
        raises a RunTimeError because that should never happen. If we're at capacity, then we
        would have expanded earlier in the function. When a location is found, the key value
        pair is written along with a bool that communicates whether the value has been "deleted".

        Gets:
            self, a Hashtable instance
            key, a string
            value, any dtype
        Returns: nothing
        """
        if not self.rehashing and self.__len__() >= self.loadfactor*self.capacity:
            self._rehash()
        hash_val = self._hash(key)
        if self.table[hash_val] == self.defVal or \
            (isinstance(self.table[hash_val], tuple) and self.table[hash_val][2] == False) or \
            (isinstance(self.table[hash_val], tuple) and self.table[hash_val][0] == key):
            self.table[hash_val] = (key, value, True)
        else:
            acceptable_loc_found = False
            iter_count = 0
            while not acceptable_loc_found:
                if iter_count >= self.capacity:
                    raise RunTimeError
                if hash_val >= self.capacity:
                    hash_val = 0
                if self.table[hash_val] == self.defVal:
                    acceptable_loc_found = True
                    self.table[hash_val] = (key, value, True)
                if self.table[hash_val] != self.defVal:
                    if not self.table[hash_val][2]:
                        acceptable_loc_found = True
                        self.table[hash_val] = (key, value, True)
                    if self.table[hash_val][0] == key:
                        self.table[hash_val] = (key, value, True)
                hash_val += 1
                iter_count += 1


    def __delitem__(self, key):
        """
        __delitem__(self, key)
        Takes in a key and "deletes" the element by changing the bool at the 3rd index
        to False. First checks the initially computed hash_val index, and if the key 
        is found there then the tuple is left in place but the bool is changed to False.
        If it's not found, we scroll until we find an empty space or a match.
        If it's found, we return it. Otherwie, throw a KeyError

        Gets: 
            self, a Hashtable instance
            key, a string
        Returns: nothing
        """
        hash_val = self._hash(key)
        if self.table[hash_val] != self.defVal and (isinstance(self.table[hash_val], tuple) and
                                                    self.table[hash_val][0] == key and
                                                    self.table[hash_val][2] == True):
            self.table[hash_val] = (self.table[hash_val][0], self.table[hash_val][1], False)
        else:
            key_found = False
            iter_count = 0
            while not key_found:
                if hash_val >= self.capacity:
                    hash_val = 0
                if self.table[hash_val] == self.defVal:
                	raise KeyError
                if self.table[hash_val] != self.defVal:
                    if self.table[hash_val][0] == key:
                        if self.table[hash_val][2] == True:
                            self.table[hash_val] = (self.table[hash_val][0], 
                                                    self.table[hash_val][1], False)
                            key_found = True
                            break
                hash_val += 1
                iter_count += 1



    def __contains__(self, key):
        """
        ___contains__(self, key)
        Checks whether the key is inside of the list of keys in the table.

        Gets: 
            self, a Hashtable instance
            key, a string
        Returns: a bool
        """
        return key in self.keys()



    def keys(self):
        """
        keys(self)
        Returns a list of the keys in the table

        Gets: self, a Hashtable instance
        Returns: a list
        """
        return [val[0] for val in  self.table if val != self.defVal and val[2]]
    
    def values(self):
        """
        keys(self)
        Returns a list of the values in the table

        Gets: self, a Hashtable instance
        Returns: a list
        """
        return [val[1] for val in self.table if val != self.defVal and val[2]]


    def __len__(self):
        """
        ___len__(self)
        Returns the number of values in the table

        Gets: self, a Hashtable instance
        Returns: a list
        """
        return len([val for val in self.table if val != self.defVal and val[2]])
    

    def __bool__(self):
        """
        __bool__(self)
        Returns whether the table is empty or not. If it is, returl False, 
        otherwise return True.

        Gets: self, a Hashtable instance
        Returns: a bool
        """
        if self.__len__() == 0:
            return False
        return True


    def __iter__(self):
        """
        __iter__(self)
        Returns an iterator of the key, value pairs in the table. 
        
        Gets: self, a Hashtable instance
        Returns: a generator
        """
        for val in self.table:
            if val != self.defVal and val[2]:
                yield (val[0], val[1])