from abc import ABC, ABCMeta, abstractmethod

class Map(ABC):
    '''
    Map is an Abstract Base class that represents an symbol table 
    ''' 

    @abstractmethod
    def __getitem__(self,key):
        '''
        Similiar to the __getitem__ method for a Python dictionary, this will 
        return the value associated with key in the map. 
        '''
        pass 

    @abstractmethod
    def __setitem__(self,key,value):
        ''' 
        Similiar to the __setitem__ method for a Python dictionary, this will 
        add or update the key-value pairing inside the map. 
        ''' 
        pass 

    @abstractmethod
    def __delitem__(self,key):
        '''
        Similiar to the __delitem__ method for a Python dictionary, this will 
        remove the key-value pairing inside the map. 
        ''' 
        pass 

    @abstractmethod
    def __contains__(self, key):
        ''' 
        Similiar to the __contains__ method for a Python dictionary, this will 
        return true if the key-value pairing is inside the map; otherwise, if not
        then return false. 
        '''
        pass 

    @abstractmethod
    def keys(self):
        '''
        Returns an iterable object (of your choosing) with all the keys inside 
        the map.
        ''' 
        pass 
    
    @abstractmethod 
    def values(self):
        ''' 
        Returns an iterable object (of your choosing) with all the values inside
        the map. 
        ''' 
        pass 

    @abstractmethod
    def __len__(self):
        '''   
           Returns the number  items in the map. 
           It needs no parameters and returns an integer.
        ''' 
        pass 
    
    @abstractmethod
    def __bool__(self):
        '''   
           Returns whether the map is empty or not. 
           it needs no parameters and returns a bool.
        ''' 
        pass 

    @abstractmethod
    def __iter__(self):
        '''   
           Returns an iterator of the objects inside the map. The iterator returns 
           the key-value pair as tuple. 
        ''' 
        pass 