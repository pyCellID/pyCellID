#%%
import io #hay que renombrar load_data.py
import images
#%%
from types import ClassMethodDescriptorType


class Data(object):
    ''''
    Clase Data es un constructor para .io
    Extiende funcionalidades de Pandas
    '''
    def __init__(self, data):
        super(Data, self).__init__()
        self.data = data


    def __repr__(self):
        return type(self)

    def __str__(self):  
        return type(self)


##########################################################################
import pandas as pd
class A(object):
    def __init__(self, nombre):
        super().__setattr__("nombre", nombre)
        super().__setattr__("_data", {})
    def __getattr__(self, n):
        return self._data.get(n, "<UNK>")
    def __setattr__(self, n, v):
        self._data[n] = v
    def m(self):
        return 43  
        
    def __init__(self, df):
        self._df = df

    def zaraza(self):
        return 1
    
    def __getitem__(self, slice):
        return self._df.__getitem__(slice)
    
    def __getattr__(self, a):
        return getattr(self._df, a)
        
    def __repr__(self):
        return repr(self._df)
    
    def _repr_html_(self):
        return  self._df._repr_html_()
    

    
