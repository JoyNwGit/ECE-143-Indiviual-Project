# -*- coding: utf-8 -*-
"""
Created on Fri May 18 17:25:32 2018

@author: Joy Nwarueze
"""

class Tower:
    '''
    This is a simple tower class. Saves details of the coordinates that made it.
    
    Tower coordinates generally made to be used to create a rectangle.
    
    Examples of its usefulness when paired with IndivProject.py. However it can be 
    used as a standalone class.
    
    '''
    #class variables
    index =-1
    def __init__(self, xzero, yzero, xone, yone):
        #instance variables
        #print 'hello world, I am a tower'
        '''
        Uses and (X,Y) coordinate pairs. 
        Namely:
            ((xzero, yzero),(xone, yone)) 
            This will be used to draw the rectangle
            
        @param xzero: int - The starting x coordinate 
        @param yzero: int - The starting y coordinate
        @param xone: int - The ending x coordinate
        @param yone: int - The ending y coordinate
        '''
        assert isinstance(xzero, int) and isinstance(yzero, int) and isinstance(xone, int) and isinstance(yone, int), "One or more of the coordinates was not an int"
        self.xzero = xzero
        self.yzero = yzero
        self.xone = xone
        self.yone = yone
        
        #aliases of xone, yone, xzero, yzero for clarity
        self.xright = xone
        self.xleft = xzero
        self.ytop = yone
        self.ybot = yzero
        
    def get_Tower_Coords(self):
        '''
        Returns tower coordinates in a tuple: (x0,y0), (x1,y1)
        
        @return coord: tuple of ints - The coordinates of the start (xzero,yzero) and
        end points (xone, yone) of the tower rectangle
        '''
        coord = (self.xzero, self.yzero), (self.xone, self.yone)
        assert isinstance(coord, tuple), "Critical Error - Coordinate meant to pass as a tuple"
        return coord
    
    def get_Tower_Area(self):
        '''
        Returns the Area that the tower covers
        
        @return area: int - The size of the tower's coverage area
        '''
        xdelta = self.xone-self.xzero
        ydelta = self.yone-self.yzero
        area = xdelta*ydelta
        assert isinstance(area, int), "Critical Error - area meant to pass as an int"
        return area
    
    def get_Index(self):
        '''
        Returns the index of the tower in the order of when it was created. The 0th tower is the first tower created
        Useful for indexing the tower from the overall superset of rectangles/towers dictionary. 
        Use: superset[str(tower.get_Index())] to return the tower you want
        Default index is -1.
        
        @return self.index: int - The tower's index value in terms of order created
        '''
        assert isinstance(self.index, int), "Critical Error - self.index meant to pass as an int"
        return self.index
    
    def set_Index(self, index):
        '''
        Sets the index of the tower. Meant to be used just after creation to determine its index value in a superset
        of rectangles/towers dictionary.
        
        @param index: int - The index value to set the tower's index in superset of rectangle/towers dictionary
        '''
        assert isinstance(self.index, int), "Critical Error - self.index meant to pass as an int"
        self.index = index