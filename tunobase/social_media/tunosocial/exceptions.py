'''
Created on 31 Oct 2013

@author: michael
'''
class RapidLikingError(Exception):
    
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)