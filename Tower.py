# -*- coding: utf-8 -*-
"""
Created on Fri May 18 17:25:32 2018

@author: Joy Nwarueze
"""

class Tower:
    #class variables
    index =-1
    
    def __init__(self, xzero, yzero, xone, yone):
        #instance variables
        #print 'hello world, I am a tower'
        self.xzero = xzero
        self.yzero = yzero
        self.xone = xone
        self.yone = yone
        
        self.xright = xone
        self.xleft = xzero
        self.ytop = yone
        self.ybot = yzero
        
    def get_Tower_Coords(self):
        coord = (self.xzero, self.yzero), (self.xone, self.yone)
        return coord
    
    def get_Tower_Area(self):
        xdelta = self.xone-self.xzero
        ydelta = self.yone-self.yzero
        area = xdelta*ydelta
        return area
    
    def get_Index(self):
        return self.index
    
    def set_Index(self, index):
        self.index = index